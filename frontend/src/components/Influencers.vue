<template>
  <div class="influencers-container">
    <!-- Search bar for filtering influencers by category -->
    <div class="search-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by category..."
        class="search-input"
      />
    </div>

    <h2 class="page-title">All Influencers</h2>

    <!-- Error Message -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- Influencer Cards -->
    <div v-else class="influencer-cards">
      <div
        class="influencer-card"
        v-for="influencer in filteredInfluencers"
        :key="influencer.id"
      >
        <div class="influencer-card-content">
          <div class="influencer-header">
            <h3>{{ influencer.influencer_name }}</h3>
            <span class="category-badge">{{ influencer.category }}</span>
          </div>
          <p><strong>Reach:</strong> {{ formatReach(influencer.reach) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Influencers',
  data() {
    return {
      influencers: [],
      error: null,
      searchQuery: '',
    };
  },
  created() {
    this.fetchInfluencers();
  },
  computed: {
    // Filter influencers based on the search query
    filteredInfluencers() {
      return this.influencers.filter((influencer) =>
        influencer.category
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    fetchInfluencers() {
      const authToken = localStorage.getItem('authToken');
      axios
        .get('http://127.0.0.1:5000/api/influencers', {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        })
        .then((response) => {
          this.influencers = response.data.data;
        })
        .catch((error) => {
          console.error('An error occurred while fetching the influencers:', error);
          this.error = 'An error occurred while fetching the influencers. Please try again.';
        });
    },
    formatReach(reach) {
      if (reach >= 1000000) {
        return (reach / 1000000).toFixed(1) + 'M';
      }
      if (reach >= 1000) {
        return (reach / 1000).toFixed(1) + 'K';
      }
      return reach;
    },
  },
};
</script>

<style scoped>
/* Container styling */
.influencers-container {
  padding: 30px;
  background-color: #f7f9fc;
  min-height: 100vh;
}

/* Search Bar */
.search-container {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #48cae4;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  border-color: #369cb3;
  outline: none;
}

/* Page Title */
.page-title {
  font-size: 36px;
  font-weight: 700;
  color: #2b2d42;
  text-align: center;
  margin-bottom: 30px;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
}

/* Error message */
.error {
  color: red;
  font-size: 16px;
  text-align: center;
  margin-bottom: 20px;
}

/* Cards Container */
.influencer-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 20px;
}

/* Individual Influencer Card */
.influencer-card {
  background-color: #ffffff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.influencer-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

/* Card Content */
.influencer-card-content {
  padding: 10px;
}

.influencer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.influencer-header h3 {
  font-size: 22px;
  font-weight: 600;
  color: #2b2d42;
}

.category-badge {
  background-color: #48cae4;
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 14px;
  text-transform: capitalize;
}

/* Card Text */
.influencer-card-content p {
  font-size: 14px;
  color: #555;
  margin-top: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .search-input {
    width: 100%;
  }

  .page-title {
    font-size: 28px;
  }

  .influencer-cards {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 480px) {
  .influencer-cards {
    grid-template-columns: 1fr;
  }
}
</style>
