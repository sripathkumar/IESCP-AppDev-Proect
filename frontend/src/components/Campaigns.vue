<template>
  <div class="campaigns-wrapper">
    <h2 class="header-title">Browse Campaigns</h2>
    <div class="search-container">
      <input
        type="text"
        v-model="searchTerm"
        placeholder="Search by campaign name..."
        class="search-field"
      />
    </div>
    <div class="campaign-grid">
      <div 
        class="campaign-card" 
        v-for="campaignItem in filteredList" 
        :key="campaignItem.id"
      >
        <div class="card-header">
          <h3 class="card-title"><strong>{{ campaignItem.name }}</strong></h3>
        </div>
        <div class="card-description">
          <p>{{ campaignItem.description }}</p>
        </div>
        <div class="card-details">
          <p><strong>Budget:</strong> {{ formatAmount(campaignItem.budget) }}</p>
          <p><strong>Goals:</strong> {{ campaignItem.goals }}</p>
          <p><strong>Ending Date: </strong>{{ formatEndDate(campaignItem.end_date) }}</p>
          <p class="status-highlight">
              <strong>{{ campaignItem.status }}</strong>
            </p>
        </div>
        <div class="card-actions">
          <button v-if="userRole === 'sponsor'" @click="navigateToEdit(campaignItem.id)">
            <i class="fa-regular fa-pen-to-square"></i> Edit
          </button>
          <button v-if="userRole === 'sponsor'" @click="removeCampaign(campaignItem.id)">
            <i class="fa-solid fa-trash"></i> Delete
          </button>
          <button v-if="userRole === 'sponsor'" @click="createAd(campaignItem.id)">
            <i class="fa-solid fa-plus"></i> Add Ad
          </button>
        </div>
      </div>
      <p v-if="filteredList.length === 0" class="no-results">
        No campaigns match your search.
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CampaignList",
  data() {
    return {
      campaignData: [],
      searchTerm: "", // Search term for filtering
      userRole: localStorage.getItem("role"),
      loggedInSponsorId: localStorage.getItem("sponsor_id"), // Fetch sponsor ID
    };
  },
  created() {
    this.loadCampaigns();
  },
  computed: {
    filteredList() {
      return this.campaignData.filter((campaignItem) => {
        // For influencers, only show public campaigns
        if (this.userRole === "influencer" && campaignItem.visibility !== "public") {
          return false;
        }
        // Filter campaigns by search term
        return campaignItem.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      });
    },
  },
  methods: {
    loadCampaigns() {
      const authToken = localStorage.getItem("authToken");
      axios
        .get(`http://127.0.0.1:5000/api/campaign?sponsor_id=${this.loggedInSponsorId}`, {
          headers: { Authorization: authToken },
        })
        .then((response) => {
          this.campaignData = response.data.data;
        })
        .catch((error) => {
          console.error("Error loading campaigns:", error);
        });
    },
    formatAmount(budget) {
      return `${(budget / 1000).toFixed(1)}k`;
    },
    formatEndDate(dateStr) {
      const date = new Date(dateStr);
      const options = { year: "numeric", month: "long", day: "2-digit" };
      return date.toLocaleDateString(undefined, options);
    },
    removeCampaign(id) {
      const authToken = localStorage.getItem("authToken");
      if (!authToken) {
        alert("Please log in to perform this action.");
        return;
      }

      axios
        .delete(`http://127.0.0.1:5000/api/campaign/${id}`, {
          headers: { Authorization: authToken },
        })
        .then(() => {
          alert("Campaign deleted successfully");
          this.loadCampaigns(); // Refresh campaign data
        })
        .catch((error) => {
          console.error("Error deleting campaign:", error);
          alert("Failed to delete campaign");
        });
    },
    navigateToEdit(id) {
      this.$router.push({ name: "EditCampaign", params: { id } });
    },
    createAd(id) {
      this.$router.push({ name: "AddingAd", params: { id } });
    },
  },
};
</script>

<style scoped>
/* Updated styles */
.campaigns-wrapper {
  padding: 30px;
  background: linear-gradient(135deg, #e3f2fd, #e1f5fe);
  min-height: 100vh;
}

.header-title {
  color: #0288d1;
  font-weight: 700;
  font-size: 34px;
  text-align: center;
  margin-bottom: 25px;
}

.search-container {
  margin-bottom: 25px;
  display: flex;
  justify-content: center;
}

.search-field {
  width: 100%;
  max-width: 450px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 10px;
  font-size: 16px;
}

.campaign-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 25px;
  justify-content: center;
}

.campaign-card {
  background: #ffffff;
  border: 1px solid #ddd;
  border-radius: 15px;
  width: 320px;
  padding: 25px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.campaign-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.card-header {
  margin-bottom: 15px;
}

.card-title {
  font-size: 1.3em;
  color: #444;
  text-align: center;
}

.card-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}

.card-details {
  font-size: 13px;
  color: #555;
  margin-bottom: 15px;
}

.card-actions {
  text-align: center;
}

button {
  background-color: #007acb;
  color: white;
  border: none;
  padding: 8px 16px;
  font-size: 13px;
  border-radius: 6px;
  cursor: pointer;
  margin: 5px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #005a91;
}

.no-results {
  color: #777;
  text-align: center;
  font-size: 15px;
}

.status-highlight {
  color: #0056b3;
  font-weight: bold;
  font-size: 15px;
  margin-top: 8px;
  text-align: center;
  background: #e3f2fd;
  padding: 6px;
  border-radius: 6px;
}
</style>
