<template>
  <div class="requests-section">
    <h2 class="page-title">Influencer Requests</h2>
    <div class="table-wrapper">
      <table class="requests-table">
        <thead>
          <tr>
            <th>Influencer ID</th>
            <th>Full Name</th>
            <th>Category</th>
            <th>Specialization</th>
            <th>Audience Reach</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="influencerItem in influencerList" :key="influencerItem.id">
            <td>{{ influencerItem.influencer_id }}</td>
            <td>{{ influencerItem.influencer_name }}</td>
            <td>{{ influencerItem.category }}</td>
            <td>{{ influencerItem.niche }}</td>
            <td>{{ influencerItem.reach }}</td>
            <td>
              <button @click="removeInfluencer(influencerItem.influencer_id)" class="action-btn remove-btn">
                <i class="fa-solid fa-trash"></i> Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminInfluencers',
  data() {
    return {
      influencerList: []  // Renamed from 'influencers'
    };
  },
  methods: {
    fetchInfluencers() {
      axios.get('http://127.0.0.1:5000/api/influencers', {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.influencerList = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching influencer requests:', error);
      });
    },

    removeInfluencer(influencerId) {
      axios.delete(`http://127.0.0.1:5000/api/influencer/${influencerId}`, {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        this.fetchInfluencers();
        alert('Influencer successfully removed');
      })
      .catch(error => {
        console.error('Error removing influencer:', error);
      });
    }
  },
  created() {
    this.fetchInfluencers();  // fetch influencers on page load
  }
};
</script>

<style scoped>
/* General styles for the section */
.requests-section {
  padding: 30px;
  background-color: #fafafa;
  border-radius: 12px;
}

.page-title {
  font-family: 'Helvetica', sans-serif;
  color: #333;
  text-align: center;
  margin-bottom: 25px;
  font-size: 28px;
  font-weight: bold;
}

/* Table styling */
.table-wrapper {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
}

.requests-table th, .requests-table td {
  padding: 16px 18px;
  text-align: left;
  font-size: 15px;
}

.requests-table th {
  background-color: #00796b;
  color: #ffffff;
}

.requests-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.requests-table tr:hover {
  background-color: #e0f2f1;
}

/* Button styles */
.action-btn {
  padding: 10px 15px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.remove-btn {
  background-color: #f44336;
  color: #ffffff;
  border: none;
}

.remove-btn:hover {
  background-color: #d32f2f;
}

.remove-btn i {
  margin-right: 8px;
}
</style>
