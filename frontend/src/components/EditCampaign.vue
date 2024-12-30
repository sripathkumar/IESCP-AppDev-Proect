<template>
  <div class="edit-campaign">
    <div class="header">
      <button class="btn back-btn" @click="navigateTo('/sponsor-dashboard')">← Back</button>
      <button class="btn logout-btn" @click="logout">Logout</button>
    </div>
    <div class="card">
      <h2>Edit Campaign</h2>
      <form @submit.prevent="submitCampaign">
        <div class="form-group">
          <label for="name">Campaign Name</label>
          <input type="text" id="name" v-model="name" placeholder="Enter campaign name" required />
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea id="description" v-model="description" placeholder="Provide a short description" required></textarea>
        </div>
        <div class="form-group">
          <label for="start-date">Start Date</label>
          <input type="date" id="start-date" v-model="start_date" required />
        </div>
        <div class="form-group">
          <label for="end-date">End Date</label>
          <input type="date" id="end-date" v-model="end_date" required />
        </div>
        <div class="form-group">
          <label for="budget">Budget</label>
          <input type="number" id="budget" v-model="budget" placeholder="Enter budget amount" required />
        </div>
        <div class="form-group">
          <label for="visibility">Visibility</label>
          <input type="text" id="visibility" v-model="visibility" placeholder="e.g., Public or Private" required />
        </div>
        <div class="form-group">
          <label for="goals">Goals</label>
          <textarea id="goals" v-model="goals" placeholder="Define campaign goals" required></textarea>
        </div>
        <button type="submit" class="btn update-btn" @click="updatecampaign(id)">Update Campaign</button>
      </form>
      <p v-if="message" class="feedback">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditCampaign',
  data() {
    return {
      sponsor_id: localStorage.getItem('sponsor_id'),
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      budget: '',
      visibility: '',
      goals: '',
      message: '',
      id: null,
      campaign: [],
    };
  },
  created() {
    this.id = this.$route.params.id;
    const token = localStorage.getItem('authToken');
    if (!token) {
      this.$router.push('/login');
    }
    this.fetchCampaign(this.id);
  },
  methods: {
    navigateTo(path) {
    this.$router.push(path); // Use Vue Router to navigate to the specified path
  },
    fetchCampaign(id) {
      const authToken = localStorage.getItem('authToken');
      axios
        .get(`http://127.0.0.1:5000/api/campaign/${id}`, {
          headers: {
            Authorization: authToken,
          },
        })
        .then((response) => {
          const campaign = response.data.data;
          this.campaign = campaign;
          this.name = campaign.name;
          this.description = campaign.description;
          this.start_date = campaign.start_date;
          this.end_date = campaign.end_date;
          this.budget = campaign.budget;
          this.visibility = campaign.visibility;
          this.goals = campaign.goals;
        })
        .catch((error) => {
          console.error('Error fetching campaign:', error);
        });
    },
    updatecampaign(id) {
      const authToken = localStorage.getItem('authToken');
      axios
        .put(
          `http://127.0.0.1:5000/api/campaign/${id}`,
          {
            name: this.name,
            sponsor_id: this.sponsor_id,
            description: this.description,
            start_date: this.start_date,
            end_date: this.end_date,
            budget: this.budget,
            visibility: this.visibility,
            goals: this.goals,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              Authorization: authToken,
            },
          }
        )
        .then(() => {
          this.message = 'Campaign updated successfully.';
          this.$router.push('/sponsor-dashboard');
        })
        .catch((error) => {
          console.error(error);
          this.message = error.response ? error.response.data.message : 'An error occurred.';
        });
    },
  },
};
</script>

<style>
/* Layout and container styles */
.edit-campaign {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 20px;
}

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
}

.card {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 100%;
  text-align: center;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

/* Form styles */
form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  text-align: left;
}

label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
  display: block;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

textarea {
  resize: none;
  height: 80px;
}

/* Button styles */
.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 8px;
  background-color: #007bff;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}

.back-btn {
  background-color: #6c757d;
}

.back-btn:hover {
  background-color: #5a6268;
}

.feedback {
  margin-top: 15px;
  font-size: 14px;
  color: #28a745;
}
</style>
