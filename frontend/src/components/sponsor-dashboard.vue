<template>
  <div class="dashboard">
    <div class="header-buttons">
      <button @click="handleLogout">Logout</button>
    </div>
    <h1 class="dashboard-title">Sponsor Dashboard</h1>
    <div class="dashboard-content">
      <div class="sidebar">
        <div class="nav-buttons">
          <button @click="showAddingCampPage">Add Campaign</button>
          <button @click="showAdRequestsPage">Ad Requests</button>
          <button @click="showCampaignsPage">Campaigns</button>
          <button @click="showAdsPage">Ads</button>
          <button @click="showInfluencerPage">Influencers</button>
          <button @click="downloadSponsorReport">Download Report</button>
        </div>
      </div>
      <div class="main-content">
        <!-- About Sponsify card -->
        <div v-if="isDefaultCardVisible" class="about-card">
          <h3>About Sponsify</h3>
          <p>Sponsify connects sponsors with influencers for effective advertising. Our mission is to simplify the process for sponsors to find influencers and for influencers to collaborate with top-tier sponsors. Explore, track, and manage campaigns effortlessly!</p>
        </div>
        <AddingCamp v-if="isAddingCampVisible" />
        <Campaigns v-if="isCampaignsVisible" />
        <Influencers v-if="isInfluencersVisible" />
        <All_Ad v-if="isAdsVisible" />
        <AdRequests v-if="isAdRequestsVisible" />
        <Pay v-if="isPayVisible" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import AddingCamp from '@/components/AddingCamp.vue';
import Campaigns from '@/components/Campaigns.vue';
import Influencers from '@/components/Influencers.vue';
import All_Ad from '@/components/All_Ad.vue';
import AdRequests from '@/components/AdRequests.vue';
import Pay from '@/components/Pay.vue';

export default {
  components: {
    AddingCamp,
    Campaigns,
    Influencers,
    All_Ad,
    AdRequests,
    Pay
    },
  data() {
    return {
      sponsorId: localStorage.getItem('sponsor_id'),
      isDefaultCardVisible: true,
      isAddingCampVisible: false,
      isCampaignsVisible: false,
      isInfluencersVisible: false,
      isAdsVisible: false,
      isAdRequestsVisible: false,
      isPayVisible: false,
      isPaymentVisible: false,
    };
  },
  methods: {
    showAdRequestsPage() {
      this.isDefaultCardVisible = false;
      this.isCampaignsVisible = false;
      this.isAddingCampVisible = false;
      this.isInfluencersVisible = false;
      this.isAdsVisible = false;
      this.isAdRequestsVisible = true;
      this.isPayVisible = true;
      this.isPaymentVisible = false;
    },
    showAddingCampPage() {
      this.isDefaultCardVisible = false;
      this.isAddingCampVisible = true;
      this.isCampaignsVisible = false;
      this.isInfluencersVisible = false;
      this.isAdsVisible = false;
      this.isAdRequestsVisible = false;
      this.isPayVisible = false;
      this.isPaymentVisible = false;
    },
    showAdsPage() {
      this.isDefaultCardVisible = false;
      this.isAddingCampVisible = false;
      this.isCampaignsVisible = false;
      this.isInfluencersVisible = false;
      this.isAdsVisible = true;
      this.isAdRequestsVisible = false;
      this.isPayVisible = false;
      this.isPaymentVisible = false;
    },
    showCampaignsPage() {
      this.isDefaultCardVisible = false;
      this.isAddingCampVisible = false;
      this.isCampaignsVisible = true;
      this.isInfluencersVisible = false;
      this.isAdsVisible = false;
      this.isAdRequestsVisible = false;
      this.isPayVisible = false;
      this.isPaymentVisible = false;
    },
    showInfluencerPage() {
      this.isDefaultCardVisible = false;
      this.isAddingCampVisible = false;
      this.isCampaignsVisible = false;
      this.isInfluencersVisible = true;
      this.isAdsVisible = false;
      this.isAdRequestsVisible = false;
      this.isPayVisible = false;
      this.isPaymentVisible = false;
    },
    showPaymentPage() {
      this.isDefaultCardVisible = false;
      this.isAddingCampaignVisible = false;
      this.isCampaignsVisible = false;
      this.isInfluencersVisible = false;
      this.isAdsVisible = false;
      this.isAdRequestsVisible = false;
      this.isPayVisible = false;
      this.isPaymentVisible = true;
    },
    async downloadSponsorReport() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/export-csv', {
          sponsor_id: this.sponsorId, // Pass the sponsor ID
        });
        alert('The report is being generated. You will receive an email once it is ready.');
      } catch (error) {
        console.error('Error generating report:', error);
      }
    },
    handleLogout() {
      localStorage.clear();
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.dashboard {
  background-color: #faf3e0;
  display: flex;
  flex-direction: column;
}

.header-buttons {
  display: flex;
  justify-content: flex-end;
  padding: 12px;
}

.header-buttons button {
  background-color: #2e6b47;
  color: #fff;
  border: none;
  padding: 12px;
  margin-left: 12px;
  border-radius: 20px;
  cursor: pointer;
}

.header-buttons button:hover {
  background-color: #7a5e42;
}

.dashboard-title {
  text-align: center;
  font-family: 'Lora', serif;
  color: #2e6b47;
  font-size: 2rem;
  margin-top: 20px;
}

.dashboard-content {
  display: flex;
  flex: 1;
  margin-top: 20px;
}

.sidebar {
  width: 20vw;
  background-color: #c89b72;
  padding: 25px;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  margin-top: 20px;
  height: 80vh;
}

.nav-buttons button {
  background-color: #2e6b47;
  color: #fff;
  border: none;
  padding: 12px;
  margin: 12px 0;
  border-radius: 20px;
  cursor: pointer;
  width: 100%;
}

.nav-buttons button:hover {
  background-color: #ddd;
}

.main-content {
  width: 75vw;
  margin: 20px;
  padding: 20px;
  border-radius: 20px;
  background-color: white;
  height: 90vh;
  overflow: scroll;
  scrollbar-color: rgb(61, 57, 48) grey;
  scrollbar-width: thin;
}

.about-card {
  background-color: #fff;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.about-card h3 {
  color: #2e6b47;
  font-family: 'Lora', serif;
}

.about-card p {
  color: #444;
  font-size: 18px;
}
</style>
