<template>
  <div class="home">
    <Navbar />
    <div class="content">
      <div class="card">
        <div class="card-body">
          <h4 class="welcome-title">
            Welcome to Our Platform
          </h4>
          <p class="card-text">
            A comprehensive solution to streamline your influencer campaigns, enabling efficient collaboration 
            between brands and creators. Let us help you achieve your goals with ease and precision.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'HomeView',
  components: {
    Navbar,
  },
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(135deg, #ffe4e1, #f5ebe0, #e8e8e4);
  font-family: 'Poppins', sans-serif;
}

.content {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  flex-grow: 1;
}

.card {
  width: 100%;
  max-width: 600px;
  background: #ffffff;
  box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.15);
  border-radius: 20px;
  text-align: center;
  padding: 30px;
}

.card-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.welcome-title {
  font-size: 24px;
  color: #283618;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-text {
  font-size: 16px;
  color: #606060;
  line-height: 1.6;
  margin: 0;
  text-align: justify;
}

@media screen and (max-width: 768px) {
  .card {
    padding: 20px;
  }

  .welcome-title {
    font-size: 20px;
  }

  .card-text {
    font-size: 14px;
  }
}
</style>
