<template>
  <div class="campaign-section">
    <h2 class="section-title">Campaign Overview</h2>
    <table class="table custom-table">
      <thead>
        <tr>
          <th scope="col">Campaign ID</th>
          <th scope="col">Name</th>
          <th scope="col">Sponsor</th>
          <th scope="col">Start Date</th>
          <th scope="col">End Date</th>
          <th scope="col">Budget</th>
          <th scope="col">Current Status</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="campaignDetail in campaignList" :key="campaignDetail.id">
          <td>{{ campaignDetail.id }}</td>
          <td>{{ campaignDetail.name }}</td>
          <td>{{ campaignDetail.sponsor_id }}</td>
          <td>{{ formatDate(campaignDetail.start_date) }}</td>
          <td>{{ formatDate(campaignDetail.end_date) }}</td>
          <td>{{ campaignDetail.budget | currency }}</td>
          <td>{{ campaignDetail.status }}</td>
          <td>
            <button 
              v-if="campaignDetail.status === 'approved'" 
              @click="toggleCampaignStatus(campaignDetail, 'rejected')" 
              class="btn btn-warning" 
              style="font-size: 14px; margin: 5px;">
              <i class="fa-solid fa-flag"></i> Flag Campaign
            </button>
            <button 
              v-else 
              @click="toggleCampaignStatus(campaignDetail, 'approved')" 
              class="btn btn-primary" 
              style="font-size: 14px; margin: 5px;">
              <i class="fa-solid fa-check"></i> Unflag Campaign
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CampaignRequest',
  data() {
    return {
      campaignList: [],
    };
  },
  methods: {
    fetchCampaignData() {
      axios.get('http://127.0.0.1:5000/api/campaign', {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.campaignList = response.data.data;
      })
      .catch(error => {
        console.error('Error fetching campaign data:', error);
      });
    },
    toggleCampaignStatus(campaignDetail, status) {
      axios.put(`http://127.0.0.1:5000/api/campaignUpdate/${campaignDetail.id}`, { status }, {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        // Update status locally
        campaignDetail.status = status;

        if (status === 'rejected') {
          this.alertSponsor(campaignDetail);
          alert('Campaign flagged successfully.');
        } else {
          alert('Campaign unflagged successfully.');
        }
      })
      .catch(error => {
        console.error(`Error changing status to ${status}:`, error);
      });
    },
    alertSponsor(campaignDetail) {
      axios.post('http://127.0.0.1:5000/api/notifySponsor', {
        sponsor_id: campaignDetail.sponsor_id,
        message: `Your campaign "${campaignDetail.name}" has been flagged. Please reach out to support for further details.`,
      }, {
        headers: {
          'Authorization': localStorage.getItem('authToken'),
        }
      })
      .then(() => {
        console.log('Sponsor notified successfully.');
      })
      .catch(error => {
        console.error('Error notifying sponsor:', error);
      });
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      const options = { year: 'numeric', month: 'long', day: '2-digit' };
      return date.toLocaleDateString(undefined, options);
    },
  },
  created() {
    this.fetchCampaignData();
  },
};
</script>

<style scoped>
/* Section Styling */
.campaign-section {
  padding: 40px;
  background-color: #e9f1f8;
  font-family: 'Arial', sans-serif;
  min-height: 100vh;
}

/* Table Styling */
.custom-table {
  width: 100%;
  margin-top: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px;
  text-align: left;
}

th {
  background-color: #024211;
  color: white;
}

td {
  border-bottom: 1px solid #e0e0e0;
}

/* Section Title */
.section-title {
  font-size: 32px;
  font-weight: 700;
  color: #2a3d54;
  text-align: center;
  margin-bottom: 20px;
}

/* Action Buttons */
.btn {
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-warning {
  background-color: #f39c12;
  color: white;
}

.btn-primary {
  background-color: #2ecc71;
  color: white;
}

.btn:hover {
  opacity: 0.8;
}

/* Responsive Design */
@media (max-width: 768px) {
  .custom-table {
    font-size: 14px;
  }

  .section-title {
    font-size: 28px;
  }
}

@media (max-width: 480px) {
  .custom-table {
    font-size: 12px;
  }

  .section-title {
    font-size: 24px;
  }
}
</style>
