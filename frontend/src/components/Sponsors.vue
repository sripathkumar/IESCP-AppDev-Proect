<template>
  <div class="partners-container">
    <h2 class="page-heading" v-if="partnerList.length">Explore Our Sponsors</h2>
    
    <!-- Filters and Search -->
    <div v-if="userRole === 'influencer'" class="filter-section">
      <div class="dropdown-filter">
        <label for="industryFilter">Industry:</label>
        <select v-model="currentIndustry" id="industryFilter">
          <option value="">All</option>
          <option v-for="sector in industryOptions" :key="sector" :value="sector">
            {{ sector }}
          </option>
        </select>
      </div>

      <div class="search-box">
        <label for="searchBox">Search:</label>
        <input
          v-model="industrySearch"
          id="searchBox"
          type="text"
          placeholder="Search industries (e.g., Fashion)"
          @input="applyFilters"
        />
      </div>
    </div>

    <div v-else class="no-partners">
      <p>No sponsors available.</p>
    </div>

    <div class="partner-cards">
      <div class="partner-card" v-for="partner in refinedPartners" :key="partner.id">
        <div class="partner-header">
          <h3>{{ partner.company_name }}</h3>
        </div>
        <div class="partner-content">
          <p><strong>Name:</strong> {{ partner.sponsor_name }}</p>
          <p><strong>Funding:</strong> {{ formatFunding(partner.budget) }}</p>
          <p><strong>Field:</strong> {{ partner.industry }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Partners",
  data() {
    return {
      partnerList: [],
      fetchError: null,
      userRole: localStorage.getItem("role"),
      currentIndustry: "", // Selected industry filter
      industrySearch: "", // Search term
      industryOptions: [], // Available industry filters
    };
  },
  created() {
    this.loadSponsors();
  },
  computed: {
    refinedPartners() {
      return this.partnerList.filter((partner) => {
        const matchesIndustry = this.currentIndustry ? partner.industry === this.currentIndustry : true;
        const matchesSearch = this.industrySearch
          ? partner.industry.toLowerCase().includes(this.industrySearch.toLowerCase())
          : true;

        return matchesIndustry && matchesSearch;
      });
    },
  },
  methods: {
    loadSponsors() {
      const token = localStorage.getItem("authToken");
      axios
        .get("http://127.0.0.1:5000/api/sponsors", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          this.partnerList = response.data.data || [];
          this.populateIndustries();
        })
        .catch((error) => {
          console.error("Error fetching sponsors:", error);
          this.fetchError = "Failed to retrieve sponsor data. Try again later.";
        });
    },
    populateIndustries() {
      this.industryOptions = [...new Set(this.partnerList.map((partner) => partner.industry))];
    },
    formatFunding(amount) {
      return `${parseFloat(amount).toLocaleString()} USD`;
    },
  },
};
</script>

<style scoped>
.partners-container {
  padding: 30px;
  background-color: #f4faff;
  min-height: 100vh;
}

.page-heading {
  color: #0077b6;
  font-size: 38px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 30px;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.dropdown-filter,
.search-box {
  display: flex;
  align-items: center;
}

.dropdown-filter label,
.search-box label {
  margin-right: 10px;
  font-size: 16px;
  color: #333;
}

.dropdown-filter select,
.search-box input {
  padding: 10px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background-color: #fff;
  transition: border-color 0.3s ease;
}

.dropdown-filter select:focus,
.search-box input:focus {
  border-color: #0077b6;
}

.search-box input {
  width: 220px;
}

.partner-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.partner-card {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.partner-card:hover {
  transform: translateY(-7px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.partner-header {
  background-color: #0077b6;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 20px;
}

.partner-header h3 {
  color: #ffffff;
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.partner-content {
  font-size: 14px;
  color: #444;
}

.partner-content p {
  margin: 8px 0;
}

.no-partners {
  text-align: center;
  font-size: 18px;
  color: #777;
}
</style>
