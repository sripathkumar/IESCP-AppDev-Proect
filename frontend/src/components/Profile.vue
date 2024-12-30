<template>
  <div class="profile-container">
    <div v-if="role !== 'sponsor'" class="profile-card">
      <div class="profile-header">
        <h2>{{ role }} Profile</h2>
      </div>
      <div class="profile-details">
        <p><strong>Username:</strong> {{ userDetails.username }}</p>
        <p v-if="role === 'influencer'"><strong>Category:</strong> {{ userDetails.category }}</p>
        <p v-if="role === 'influencer'"><strong>Niche:</strong> {{ userDetails.niche }}</p>
        <p v-if="role === 'influencer'"><strong>Reach:</strong> {{ userDetails.reach }}</p>
        <p v-if="role === 'sponsor'"><strong>Company:</strong> {{ userDetails.company }}</p>
        <p v-if="role === 'sponsor'"><strong>Industry:</strong> {{ userDetails.industry }}</p>
        <p v-if="role === 'sponsor'"><strong>Budget:</strong> {{ userDetails.budget }}</p>
      </div>
    </div>
    <p v-if="role === 'sponsor'" class="no-profile-message">
      Sponsor profile is currently unavailable.
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      role: localStorage.getItem("role"),
      userDetails: {},
    };
  },
  mounted() {
    this.fetchUserDetails();
  },
  methods: {
    fetchUserDetails() {
      this.userDetails = {
        username: localStorage.getItem("username"),
        category: localStorage.getItem("category"),
        niche: localStorage.getItem("niche"),
        reach: localStorage.getItem("reach"),
        company: localStorage.getItem("Company_name"),
        industry: localStorage.getItem("Industry"),
        budget: localStorage.getItem("budget"),
      };
    },
  },
};
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  padding: 40px 20px;
}

.profile-card {
  background: linear-gradient(145deg, #ffffff, #f3f3f3);
  color: #212529;
  border-radius: 20px;
  padding: 30px;
  width: 100%;
  max-width: 600px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1), 0 6px 6px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-align: left;
}

.profile-card:hover {
  transform: scale(1.02);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15), 0 8px 8px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: 20px;
}

.profile-header h2 {
  font-size: 28px;
  color: #495057;
  font-family: "Poppins", sans-serif;
  font-weight: 700;
  text-transform: capitalize;
  margin: 0;
}

.profile-details {
  font-family: "Lato", sans-serif;
  font-size: 16px;
  line-height: 1.7;
  color: #343a40;
}

.profile-details p {
  margin-bottom: 15px;
}

.profile-details strong {
  color: #007bff;
}

.no-profile-message {
  font-size: 18px;
  text-align: center;
  color: #6c757d;
  font-family: "Poppins", sans-serif;
  margin-top: 30px;
  padding: 10px 20px;
  border: 1px solid #ced4da;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
