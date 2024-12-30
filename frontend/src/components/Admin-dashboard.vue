<template>
  <div class="admin-dashboard">
    <div class="header-section">
      <h1 class="dashboard-title">Admin Dashboard</h1>
      <div class="action-buttons">
        <button @click="logoutUser">Logout</button>
      </div>
    </div>
    <div class="dashboard-body">
      <!-- Navigation Buttons -->
      <div class="nav-action-buttons">
        <button @click="displayAnalytics">Analytics</button>
        <button @click="displayAdminCamp">Campaigns</button>
        <button @click="displaySponsorRequests">Sponsor Requests</button>
        <button @click="displayAdminInfluencers">Influencers</button>
      </div>
      
      <div class="content-wrapper">
        <div class="content">
          <!-- Conditional Content Rendering -->
          <SponsorRequest v-if="showingSponsorSection" />
          <AdminInfluencers v-if="showingInfluencerSection" />
          <AdminCamp v-if="showingCampaignSection" />
          <Analytics v-if="showingAnalyticsSection" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SponsorRequest from '@/components/SponsorRequest.vue';
import AdminInfluencers from '@/components/AdminInfluencers.vue';
import AdminCamp from '@/components/AdminCamp.vue';
import Analytics from '@/components/Analytics.vue';

export default {
  name: 'AdminDashboardPage',
  components: {
    SponsorRequest,
    AdminInfluencers,
    AdminCamp,
    Analytics
  },
  data() {
    return {
      showingSponsorSection: false,
      showingInfluencerSection: false,
      showingCampaignSection: false,
      showingAnalyticsSection: true,
    };
  },
  methods: {
    logoutUser() {
      localStorage.clear();
      this.$router.push('/login');
    },
    displaySponsorRequests() {
      this.showingSponsorSection = true;
      this.showingInfluencerSection = false;
      this.showingCampaignSection = false;
      this.showingAnalyticsSection = false;
    },
    displayAdminInfluencers() {
      this.showingSponsorSection = false;
      this.showingInfluencerSection = true;
      this.showingCampaignSection = false;
      this.showingAnalyticsSection = false;
    },
    displayAdminCamp() {
      this.showingSponsorSection = false;
      this.showingInfluencerSection = false;
      this.showingCampaignSection = true;
      this.showingAnalyticsSection = false;
    },
    displayAnalytics() {
      this.showingAnalyticsSection = true;
      this.showingSponsorSection = false;
      this.showingInfluencerSection = false;
      this.showingCampaignSection = false;
    }
  }
};
</script>

<style scoped>
/* General Dashboard Styling */
.admin-dashboard {
  background-color: #f7f1e1;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* Header Styling */
.header-section {
  display: flex;
  justify-content: space-between;
  padding: 15px;
  background-color: #8d5a4e;
  color: white;
  border-radius: 20px;
}

.dashboard-title {
  font-family: 'Headland One', serif;
  color: #2d4c32;
}

.action-buttons {
  display: flex;
}

.action-buttons button {
  background-color: #2d4c32;
  color: #fff;
  border: none;
  padding: 12px 18px;
  margin-left: 15px;
  border-radius: 20px;
  cursor: pointer;
}

.action-buttons button:hover {
  background-color: #6b3f2d;
}

/* Navigation Buttons Styling */
.nav-action-buttons {
  display: flex;
  justify-content: space-around;
  background-color: #8d5a4e;
  padding: 15px;
  border-radius: 20px;
}

.nav-action-buttons button {
  background-color: #2d4c32;
  color: white;
  border: none;
  padding: 12px 18px;
  margin: 5px;
  border-radius: 20px;
  cursor: pointer;
  flex: 1;
}

.nav-action-buttons button:hover {
  background-color: #d8cfd8;
}

/* Main Content Styling */
.dashboard-body {
  display: flex;
  flex-direction: column;
  padding: 20px;
  flex-grow: 1;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.content {
  margin: 20px;
  padding: 20px;
  border-radius: 20px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 150px);
  overflow-y: auto;
}

/* Badge for Notifications */
.badge {
  background-color: #e74c3c;
  color: white;
  border-radius: 50%;
  padding: 6px;
  font-size: 14px;
}
</style>
