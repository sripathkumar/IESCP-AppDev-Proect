<template>
  <div class="campaign-container">
    <div class="header-section">
      <h2>Create a New Advertising Campaign</h2>
    </div>
    <form @submit.prevent="handleCampaignSubmission" class="campaign-form">
      <div class="input-group">
        <label for="campaign-name">Campaign Title:</label>
        <input type="text" id="campaign-name" v-model="campaignTitle" placeholder="Enter campaign title" required>
      </div>
      <div class="input-group">
        <label for="campaign-description">Campaign Details:</label>
        <textarea id="campaign-description" v-model="campaignDetails" placeholder="Describe the campaign" required></textarea>
      </div>
      <div class="input-group">
        <label for="start-date">Start Date:</label>
        <input type="date" id="start-date" v-model="startDate" required>
      </div>
      <div class="input-group">
        <label for="end-date">End Date:</label>
        <input type="date" id="end-date" v-model="endDate" required>
      </div>
      <div class="input-group">
        <label for="budget">Budget (USD):</label>
        <input type="number" id="budget" v-model="campaignBudget" placeholder="Enter campaign budget" required>
      </div>
      <div class="input-group">
        <label for="visibility">Visibility:</label>
        <select id="visibility" v-model="visibility" required>
          <option value="" disabled>Select visibility level</option>
          <option value="public">Public</option>
          <option value="private">Private</option>
        </select>
      </div>
      <div class="input-group">
        <label for="campaign-goals">Campaign Goals:</label>
        <input type="text" id="campaign-goals" v-model="campaignGoals" placeholder="Enter goals for your campaign" required>
      </div>
      <button type="submit" class="submit-button">Create Campaign</button>
    </form>
    <div v-if="statusMessage" class="status-message">
      <p>{{ statusMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AddingCamp',
  data() {
    return {
      sponsorId: localStorage.getItem('sponsor_id'),
      campaignTitle: '',
      campaignDetails: '',
      startDate: '',
      endDate: '',
      campaignBudget: '',
      visibility: '',
      campaignGoals: '',
      statusMessage: '',
    };
  },
  methods: {
    handleCampaignSubmission() {
      const campaignData = new FormData();
      campaignData.append('name', this.campaignTitle);
      campaignData.append('sponsor_id', this.sponsorId);
      campaignData.append('description', this.campaignDetails);
      campaignData.append('start_date', this.startDate);
      campaignData.append('end_date', this.endDate);
      campaignData.append('budget', this.campaignBudget);
      campaignData.append('visibility', this.visibility);
      campaignData.append('goals', this.campaignGoals);

      const authToken = localStorage.getItem('authToken');
      if (localStorage.getItem('role') === 'sponsor') {
        axios
          .post('http://127.0.0.1:5000/api/campaign', campaignData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': authToken,
            },
          })
          .then((response) => {
            this.statusMessage = 'Campaign successfully created!';
            this.$router.push('/sponsor-dashboard');
          })
          .catch((error) => {
            console.error(error);
            this.statusMessage = error.response ? error.response.data.message : 'An error occurred. Please try again.';
          });
      } else {
        this.statusMessage = 'You do not have permission to create a campaign.';
      }
    },
  },
};
</script>

<style scoped>
.campaign-container {
  max-width: 650px;
  margin: 30px auto;
  padding: 25px;
  background-color: #e9f5f1;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.header-section {
  text-align: center;
  margin-bottom: 25px;
}

.campaign-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: bold;
  color: #333;
}

input,
textarea,
select {
  padding: 12px;
  border: 1px solid #d1d1d1;
  border-radius: 10px;
  font-size: 15px;
}

textarea {
  resize: none;
}

.submit-button {
  background-color: #007b4f;
  color: white;
  padding: 12px 18px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #005d34;
}

.status-message {
  margin-top: 25px;
  padding: 15px;
  background-color: #d4f0d4;
  border: 1px solid #a3f0a3;
  border-radius: 10px;
  color: #317531;
  font-weight: bold;
}
</style>
