<template>
  <div class="ad-page">
    <h1 class="page-title">Advertisements</h1>
    
    <div class="filter-container">
      <input 
        v-model="searchQuery" 
        @input="searchAds" 
        type="text" 
        class="search-input" 
        placeholder="Search by keyword (e.g., tech)"
      />
      
      <select v-model="selectedCampaign" class="campaign-filter">
        <option value="">Filter by Campaign</option>
        <option v-for="campaign in campaigns" :key="campaign.id" :value="campaign.id">{{ campaign.name }}</option>
      </select>
    </div>
    
    <div v-if="ads.length" class="ads-container">
      <div v-for="ad in filteredAds" :key="ad.id" class="ad-card">
        <div class="ad-card-header">
          <h3 class="ad-title">{{ ad.name }}</h3>
          <p class="ad-campaign">{{ ad.campaignName }}</p>
        </div>
        <div class="ad-card-body">
          <p class="ad-details">
            <strong>Sponsor:</strong> {{ ad.sponsorCompanyName }}<br />
            <strong>Start Date:</strong> {{ formatDate(ad.start_date) }}<br />
          </p>

          <!-- Editable Budget Field -->
          <div class="ad-budget">
            <label for="budget">Budget: </label>
            <input 
              v-if="role === 'sponsor'" 
              type="number" 
              v-model="ad.budget" 
              class="budget-input" 
              :placeholder="formatBudget(ad.budget)"
            />
            <span v-else>{{ formatBudget(ad.budget) }}</span>
          </div>
        </div>
        
        <div class="ad-actions">
          <button v-if="role === 'sponsor'" @click="editAd(ad.id)" class="btn-edit">Edit</button>
          <button v-if="role === 'sponsor'" @click="deleteAd(ad.id)" class="btn-delete">Delete</button>

          <div v-if="role === 'sponsor'" class="send-request">
            <label for="influencer-select">Send Request to Influencer</label>
            <select v-model="selectedInfluencer[ad.id]" @change="selectInfluencer(ad.id, $event)" class="influencer-select">
              <option v-for="influencer in influencers" :key="influencer.influencer_id" :value="influencer.influencer_id">
                {{ influencer.influencer_name }}
              </option>
            </select>
            <button @click="sendAdRequest(ad.id)" class="btn-send-request">Send</button>
          </div>

          <div v-if="role === 'influencer'" class="send-request">
            <label for="sponsor-select">Send Request to Sponsor</label>
            <select v-model="selectedSponsor[ad.id]" @change="selectSponsor(ad.id, $event)" class="sponsor-select">
              <option v-for="sponsor in sponsors" :key="sponsor.sponsor_id" :value="sponsor.sponsor_id">
  {{ sponsor.company_name || sponsor.sponsor_name }}
</option>
            </select>
            <button @click="sendAdRequest(ad.id)" class="btn-send-request">Send</button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else>
      <p>No ads available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'All_Ad',
  data() {
    return {
      role: localStorage.getItem('role'),
      ads: [],
      campaigns: [],
      influencers: [],
      sponsors: [],
      searchQuery: '',
      selectedCampaign: '',
      selectedInfluencer: {},
      selectedSponsor: {},
      filteredAds: []
    };
  },
  created() {
    this.fetchCampaigns();
    this.fetchInfluencers();
    this.fetchSponsors();
    this.fetchAds();
  },
  methods: {
    async fetchAds() {
  const token = localStorage.getItem('authToken');
  let url = 'http://127.0.0.1:5000/api/Ad';
  if (this.selectedCampaign) {
    url += `?campaign_id=${this.selectedCampaign}`;
  }

  try {
    const response = await axios.get(url, {
      headers: {
        Authorization: token,
      },
    });
    this.ads = response.data.data;
    await this.populateAdditionalInfo();

    // Apply visibility filter for influencers
    if (this.role === 'influencer') {
      this.filteredAds = this.ads.filter(ad => {
        const campaign = this.campaigns.find(campaign => campaign.id === ad.campaign_id);
        return campaign && campaign.visibility === 'public'; // Exclude private campaigns
      });
    } else {
      // Sponsors can see all ads
      this.filteredAds = this.ads;
    }
  } catch (error) {
    console.error('Error fetching ads:', error);
  }
},
    async populateAdditionalInfo() {
      const token = localStorage.getItem('authToken');
      for (const ad of this.ads) {
        try {
          const campaignResponse = await axios.get(`http://127.0.0.1:5000/api/campaign/${ad.campaign_id}`, {
            headers: { 'Authorization': token }
          });
          ad.campaignName = campaignResponse.data.data.name;

          const sponsorResponse = await axios.get(`http://127.0.0.1:5000/api/sponsor/${ad.sponsor_id}`, {
            headers: { 'Authorization': token }
          });
          ad.sponsorCompanyName = sponsorResponse.data.data.company_name;
        } catch (error) {
          console.error('Error fetching additional info:', error);
        }
      }
    },
    searchAds() {
  const baseAds = this.role === 'influencer'
    ? this.ads.filter(ad => {
        const campaign = this.campaigns.find(campaign => campaign.id === ad.campaign_id);
        return campaign && campaign.visibility === 'public'; // Only public ads for influencers
      })
    : this.ads;

  this.filteredAds = baseAds.filter(ad =>
    ad.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
    ad.content.toLowerCase().includes(this.searchQuery.toLowerCase())
  );
},
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
      });
    },
    formatBudget(budget) {
      return budget >= 1000 ? `${(budget / 1000).toFixed(1)}k` : budget;
    },
    selectInfluencer(adId, event) {
      this.selectedInfluencer[adId] = event.target.value;
    },
    selectSponsor(adId, event) {
      this.selectedSponsor[adId] = event.target.value;
    },
    sendAdRequest(id) {
      const token = localStorage.getItem('authToken');
      const ad = this.ads.find(ad => ad.id === id);
      const isSponsor = this.role === 'sponsor';
      const adRequestData = {
        ad_id: ad.id,
        sponsor_id: isSponsor ? localStorage.getItem('sponsor_id') : this.selectedSponsor[ad.id],
        influencer_id: isSponsor ? this.selectedInfluencer[ad.id] : localStorage.getItem('influencer_id'),
        campaign_id: ad.campaign_id,
        message: `${ad.content}\n${ad.requirements}\n${ad.budget}`,
        requirements: ad.requirements,
        payment: ad.budget // Use the updated budget here
      };

      axios.post('http://127.0.0.1:5000/api/ad_request', adRequestData, {
        headers: { 'Authorization': token }
      })
        .then(() => {
          alert('Ad request sent successfully!');
        })
        .catch(error => {
          console.error('Error sending ad request:', error);
        });
    },
    fetchCampaigns() {
      axios.get('http://127.0.0.1:5000/api/campaign', {
        headers: { 'Authorization': localStorage.getItem('authToken') }
      }).then(response => {
        this.campaigns = response.data.data;
      }).catch(error => {
        console.error('Error fetching campaigns:', error);
      });
    },
    fetchInfluencers() {
      axios.get('http://127.0.0.1:5000/api/influencers', {
        headers: { 'Authorization': localStorage.getItem('authToken') }
      }).then(response => {
        this.influencers = response.data.data;
      }).catch(error => {
        console.error('Error fetching influencers:', error);
      });
    },
    fetchSponsors() {
  axios.get('http://127.0.0.1:5000/api/sponsors', {
    headers: { 'Authorization': localStorage.getItem('authToken') }
  }).then(response => {
    this.sponsors = response.data.data;
  }).catch(error => {
    console.error('Error fetching sponsors:', error);
  });
},
    editAd(adId) {
      this.$router.push(`/edit-ad/${adId}`);
    },
    deleteAd(adId) {
      const token = localStorage.getItem('authToken');
      axios.delete(`http://127.0.0.1:5000/api/Ad/${adId}`, {
        headers: { 'Authorization': token }
      })
      .then(() => {
        this.fetchAds();
      })
      .catch(error => {
        console.error('Error deleting ad:', error);
      });
    }
  }
};
</script>

<style scoped>
.ad-page {
  font-family: 'Arial', sans-serif;
  margin: 20px;
}

.page-title {
  font-size: 36px;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.filter-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input, .campaign-filter {
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
  outline: none;
}

.search-input:focus, .campaign-filter:focus {
  border-color: #4CAF50;
}

.ads-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-around;
}

.ad-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 45%;
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.ad-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.ad-card-header {
  margin-bottom: 15px;
}

.ad-title {
  font-size: 24px;
  color: #333;
  font-weight: bold;
}

.ad-campaign {
  font-size: 16px;
  color: #888;
}

.ad-card-body {
  margin-bottom: 15px;
}

.ad-details {
  font-size: 16px;
  color: #555;
}

.ad-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-edit, .btn-delete, .btn-send-request {
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.btn-edit {
  background-color: #4CAF50;
  color: white;
}

.btn-edit:hover {
  background-color: #45a049;
}

.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #e53935;
}

.send-request {
  display: flex;
  flex-direction: column;
}

.influencer-select, .sponsor-select {
  padding: 8px;
  font-size: 14px;
  margin: 5px 0;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.influencer-select:focus, .sponsor-select:focus {
  border-color: #4CAF50;
}
</style>

