<template>
  <div>
    <h2 class="header-title">All your Ad Requests</h2>
    <div v-if="filteredAdRequests.length === 0" class="no-requests-message">
      No ad requests available.
    </div>
    <div class="ad-request-cards">
      <div v-for="adRequest in filteredAdRequests" :key="adRequest.id" class="ad-request-card">
        <p><strong>Campaign Name:</strong> {{ campaignNames[adRequest.campaign_id] }}</p>
        <p><strong>Ad Name:</strong> {{ adNames[adRequest.ad_id] }}</p>
        <p><strong>Sponsor Name:</strong> {{ sponsorNames[adRequest.sponsor_id] }}</p>
        <p><strong>Content:</strong> {{ adRequest.content }}</p>
        <p><strong>Requirements:</strong> {{ adRequest.requirements }}</p>
        <p><strong>Budget:</strong> {{ adRequest.budget | currency }}</p>
        <p><strong>Status:</strong> {{ adRequest.status.charAt(0).toUpperCase() + adRequest.status.slice(1) }}</p> <!-- Status Display -->
        <div class="button-group" v-if="adRequest.status === 'pending'">
          <button @click="updateAdRequestStatus(adRequest.id, 'accepted')" class="btn-accept">
            <i class="fa-solid fa-check"></i> Accept
          </button>
          <button @click="updateAdRequestStatus(adRequest.id, 'rejected')" class="btn-reject">
            <i class="fa-solid fa-xmark"></i> Reject
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdRequests',
  data() {
    return {
      adRequests: [],
      campaignNames: {},
      adNames: {},
      sponsorNames: {},
      influencerUsernames: {},  // Object to store influencer usernames
      authToken: localStorage.getItem('authToken'),
      influencerId: localStorage.getItem('influencer_id'),
      sponsorId: localStorage.getItem('sponsor_id'),
    };
  },
  computed: {
    filteredAdRequests() {
      return this.adRequests.filter(adRequest => {
        if (this.influencerId) {
          // Display accepted and rejected requests for influencer
          return adRequest.influencer_id === parseInt(this.influencerId);
        } else if (this.sponsorId) {
          // Display accepted and rejected requests for sponsor
          return adRequest.sponsor_id === parseInt(this.sponsorId);
        }
        return false;
      });
    }
  },
  methods: {
    async fetchAdRequests() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/ad_request', {
          headers: { 'Authorization': this.authToken }
        });

        this.adRequests = response.data.data.map(adRequest => ({
          id: adRequest.id,
          campaign_id: adRequest.campaign_id,
          ad_id: adRequest.ad_id,
          sponsor_id: adRequest.sponsor_id,
          content: adRequest.message,
          status: adRequest.status,
          requirements: adRequest.requirements,
          budget: adRequest.payment,
          influencer_id: adRequest.influencer_id
        }));

        // Fetch additional details for each ad request (async)
        await Promise.all(this.adRequests.map(adRequest => {
          this.fetchCampaignName(adRequest.campaign_id);
          this.fetchAdName(adRequest.ad_id);
          this.fetchSponsorName(adRequest.sponsor_id);
          return this.fetchInfluencerUsername(adRequest.influencer_id); // Ensure influencer is fetched for each request
        }));
      } catch (error) {
        console.error('Error fetching ad requests:', error);
      }
    },
    async fetchAdName(adId) {
      if (!this.adNames[adId]) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/Ad/${adId}`, { headers: { 'Authorization': this.authToken } });
          this.adNames = { ...this.adNames, [adId]: response.data.data.name };
        } catch (error) {
          console.error('Error fetching ad name:', error);
        }
      }
    },
    async fetchSponsorName(sponsorId) {
      if (!this.sponsorNames[sponsorId]) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/sponsor/${sponsorId}`, { headers: { 'Authorization': this.authToken } });
          this.sponsorNames = { ...this.sponsorNames, [sponsorId]: response.data.data.company_name };
        } catch (error) {
          console.error('Error fetching sponsor name:', error);
        }
      }
    },
    async fetchCampaignName(campaignId) {
      if (!this.campaignNames[campaignId]) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/api/campaign/${campaignId}`, { headers: { 'Authorization': this.authToken } });
          this.campaignNames = { ...this.campaignNames, [campaignId]: response.data.data.name };
        } catch (error) {
          console.error('Error fetching campaign name:', error);
        }
      }
    },
    async fetchInfluencerUsername(influencerId) {
      if (!this.influencerUsernames[influencerId]) {
        try {
          console.log(`Fetching influencer data for ID: ${influencerId}`);  // Log influencerId

          // Step 1: Get influencer data which contains user_id
          const influencerResponse = await axios.get(`http://127.0.0.1:5000/api/influencer/${influencerId}`, { headers: { 'Authorization': this.authToken } });
          const userId = influencerResponse.data.data.user_id;  // Assuming the influencer data has a field 'user_id'
          
          console.log(`Found user_id: ${userId} for influencer ${influencerId}`);

          // Step 2: Get the influencer's name from the user table using user_id
          const userResponse = await axios.get(`http://127.0.0.1:5000/api/user/${userId}`, { headers: { 'Authorization': this.authToken } });
          const influencerName = userResponse.data.data.name;  // Assuming the user data has a field 'name'
          
          console.log(`Influencer name fetched: ${influencerName}`);

          // Step 3: Store the influencer's name in the influencerUsernames object
          this.influencerUsernames = { ...this.influencerUsernames, [influencerId]: influencerName };

        } catch (error) {
          console.error('Error fetching influencer name:', error);
        }
      }
    },
    updateAdRequestStatus(adRequestId, status) {
      axios.put(`http://127.0.0.1:5000/api/ad_request/${adRequestId}`, { status }, {
        headers: { 'Authorization': this.authToken }
      })
      .then(() => {
        alert(`Ad request ${status} successfully`);
        this.fetchAdRequests();
      })
      .catch(error => console.error(`Error updating ad request status to ${status}:`, error));
    }
  },
  created() {
    this.fetchAdRequests();
  }
};
</script>

<style scoped>
.header-title {
  color: #48cae4;
  font-weight: 800;
  font-size: 36px;
  padding-bottom: 10px;
  text-align: center;
}

.no-requests-message {
  text-align: center;
  font-size: 18px;
  color: #555;
  margin-top: 20px;
}

.ad-request-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.ad-request-card {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: left;
  color: #333;
}

.ad-request-card p {
  margin: 5px 0;
}

.ad-request-card strong {
  color: #283618;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  justify-content: center;
}

button {
  padding: 10px 15px;
  font-size: 14px;
  border-radius: 5px;
  color: #fff;
  background-color: #4caf50;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #45a049;
}

.btn-reject {
  background-color: #f44336;
}

.btn-reject:hover {
  background-color: #e53935;
}
</style>
