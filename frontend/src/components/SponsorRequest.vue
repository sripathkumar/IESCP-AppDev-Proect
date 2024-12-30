<template>
  <div class="request-container mt-4">
    <h2 class="header-title mb-4">Sponsor Requests</h2>
    <table class="custom-table table-striped table-bordered table-hover">
      <thead class="table-header">
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Sponsor Name</th>
          <th scope="col">Company</th>
          <th scope="col">Industry</th>
          <th scope="col">Budget</th>
          <th scope="col">Status</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in sponsorRequests" :key="request.sponsor_id">
          <td>{{ request.sponsor_id }}</td>
          <td>{{ request.sponsor_name }}</td>
          <td>{{ request.company_name }}</td>
          <td>{{ request.industry }}</td>
          <td>{{ request.budget | currency }}</td>
          <td>
            <span :class="{
              'status-approved': request.status === 'approved',
              'status-pending': request.status === 'pending',
              'status-rejected': request.status === 'rejected'
            }">
              {{ request.status }}
            </span>
          </td>
          <td>
            <button @click="approveSponsor(request.sponsor_id)" class="btn btn-success btn-sm" style="font-size: 16px; padding: 8px;">
              <i class="fa-solid fa-check"></i> Approve
            </button>
            <button @click="rejectSponsor(request.sponsor_id)" class="btn btn-danger btn-sm" style="font-size: 16px; padding: 8px;">
              <i class="fa-solid fa-xmark"></i> Reject
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
  name: 'SponsorRequestsPage',
  data() {
    return {
      sponsorRequests: [],
      userId: "",
      userName: "",
    };
  },
  methods: {
    fetchRequests() {
      axios.get('http://127.0.0.1:5000/api/sponsors', {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.sponsorRequests = response.data.data;
        this.userId = response.data.data.user_id;
      })
      .catch(error => {
        console.error('Error fetching sponsor requests:', error);
      });
    },
    approveSponsor(sponsorId) {
      axios.put(`http://127.0.0.1:5000/api/sponsor/${sponsorId}`, { status: 'approved' }, {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        this.fetchRequests();
        alert('Sponsor approved successfully');
      })
      .catch(error => {
        console.error('Error updating sponsor status:', error);
      });
    },
    getUsername(id) {
      const authToken = localStorage.getItem('authToken');
      axios.get(`http://127.0.0.1:5000/api/user/${id}`, {
        headers: {
          'Authorization': authToken,
        },
      })
      .then(response => {
        this.userName = response.data.data.username;
      })
      .catch(error => {
        console.error('Error fetching user details:', error);
      });
    },
    rejectSponsor(sponsorId) {
      axios.delete(`http://127.0.0.1:5000/api/sponsor/${sponsorId}`, {
        headers: {
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(() => {
        this.fetchRequests();
        alert('Sponsor rejected successfully');
      })
      .catch(error => {
        console.error('Error deleting sponsor:', error);
      });
    }
  },
  created() {
    this.fetchRequests();
  }
};
</script>

<style scoped>
/* General container styles */
.request-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 30px;
}

/* Table Styling */
.custom-table {
  border-radius: 12px;
  overflow: hidden;
  font-size: 16px;
  width: 100%;
  table-layout: fixed;
}

.custom-table th, .custom-table td {
  text-align: center;
  vertical-align: middle;
  padding: 16px 20px;
}

.custom-table .table-header {
  background-color: #004d40;
  color: white;
  font-size: 18px;
}

.custom-table .status-approved {
  color: green;
}

.custom-table .status-pending {
  color: orange;
}

.custom-table .status-rejected {
  color: red;
}

.custom-table .btn {
  padding: 8px 16px;
  font-size: 16px;
}

.custom-table tbody tr:hover {
  background-color: #f4f4f4;
}

.header-title {
  font-size: 2.5rem;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

button {
  font-size: 16px;
  margin: 5px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #00796b;
}

/* Button Color */
button.approve {
  background-color: #388e3c;
}

button.reject {
  background-color: #d32f2f;
}
</style>