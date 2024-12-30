<template>
  <nav class="navbar">
    <router-link to="/register-influencer" class="nav-link">Register as Influencer</router-link>
    <router-link to="/register-brand" class="nav-link">Register as Sponsor</router-link>
    <router-link to="/login" class="nav-link">Login</router-link>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(90deg, #003d5b, #26547c);
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.nav-link {
  text-decoration: none;
  color: #ffffff;
  font-size: 1rem;
  font-weight: bold;
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, #2a9d8f, #48cae4);
  border-radius: 25px;
  transition: all 0.3s ease-in-out;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
}

.nav-link:hover {
  background: linear-gradient(135deg, #48cae4, #2a9d8f);
  transform: translateY(-3px) scale(1.1);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
}

.navbar {
  flex-wrap: wrap;
}

@media screen and (max-width: 768px) {
  .navbar {
    gap: 1rem;
    padding: 0.8rem 1rem;
  }

  .nav-link {
    font-size: 0.9rem;
    padding: 0.5rem 1rem;
  }
}
</style>
