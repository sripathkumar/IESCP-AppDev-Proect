<template>
  <div class="dashboard">
    <div class="header">
      <div class="logo">Sponsify</div>
      <div class="header-buttons">
        <button class="logout-btn" @click="logout">Logout</button>
      </div>
    </div>

    <div class="dashboard-content">
      <div class="sidebar">
        <nav class="nav-menu">
          <button class="nav-item" @click="showProfile">Profile</button>
          <button class="nav-item" @click="showCampaign">Campaigns</button>
          <button class="nav-item" @click="showSponsors">Sponsors</button>
          <button class="nav-item" @click="showAdRequest">Ad Requests</button>
          <button class="nav-item" @click="showAd">Ads</button>
        </nav>
      </div>
      <div class="main-content">
        <div v-if="defaultcard" class="welcome-card">
          <h2 class="welcome-title">Welcome to Sponsify</h2>
          <p class="welcome-text">
            Sponsify bridges the gap between influencers and brands. Explore campaigns, manage ad requests, and build impactful collaborations!
          </p>
        </div>

        <Profile v-if="showingProfile" />
        <Campaigns v-if="showingCampaign" />
        <Sponsors v-if="showingSponsors" />
        <AdRequests v-if="showingAdRequests" />
        <All_Ad v-if="showingAd" />
      </div>
    </div>
  </div>
</template>

<script>
import Profile from "@/components/Profile.vue";
import Campaigns from "@/components/Campaigns.vue";
import Sponsors from "@/components/Sponsors.vue";
import AdRequests from "@/components/AdRequests.vue";
import All_Ad from "@/components/All_Ad.vue";

export default {
  components: {
    Profile,
    Campaigns,
    Sponsors,
    AdRequests,
    All_Ad,
  },
  data() {
    return {
      showingProfile: false,
      defaultcard: true,
      showingCampaign: false,
      showingSponsors: false,
      showingAdRequests: false,
      showingAd: false,
    };
  },
  methods: {
    showProfile() {
      this.resetViews();
      this.showingProfile = true;
    },
    showCampaign() {
      this.resetViews();
      this.showingCampaign = true;
    },
    showSponsors() {
      this.resetViews();
      this.showingSponsors = true;
    },
    showAdRequest() {
      this.resetViews();
      this.showingAdRequests = true;
    },
    showAd() {
      this.resetViews();
      this.showingAd = true;
    },
    resetViews() {
      this.defaultcard = false;
      this.showingProfile = false;
      this.showingCampaign = false;
      this.showingSponsors = false;
      this.showingAdRequests = false;
      this.showingAd = false;
    },
    logout() {
      localStorage.clear();
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(to bottom, #eef2f3, #8e9eab);
  font-family: "Roboto", sans-serif;
}

.header {
  background-color: #2c3e50;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 26px;
  font-weight: bold;
  text-transform: uppercase;
}

.header-buttons .logout-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.header-buttons .logout-btn:hover {
  background-color: #c0392b;
}

.dashboard-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar {
  width: 20%;
  background-color: #34495e;
  padding: 30px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  border-radius: 0 25px 25px 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 15px;
}

.nav-item {
  background: #2ecc71;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: #27ae60;
  transform: scale(1.05);
}

.main-content {
  width: 80%;
  background: white;
  margin: 20px;
  padding: 30px;
  border-radius: 25px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
}

.welcome-card {
  text-align: center;
  background: #f7f9fa;
  padding: 40px;
  border-radius: 25px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.welcome-title {
  color: #2c3e50;
  font-size: 28px;
  margin-bottom: 15px;
}

.welcome-text {
  color: #34495e;
  font-size: 18px;
  line-height: 1.6;
}
</style>
