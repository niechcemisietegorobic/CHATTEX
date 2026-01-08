<script lang="ts" setup>
import { ref } from 'vue';
import { API_URL } from '@/constants';

const props = defineProps(["is_logged", "username"])
const emit = defineEmits(["updateIsLogged", "updateUsername"])

const register_visible = ref(false)
const field_username = ref('')
const password = ref('')

async function register() {
  const r = await fetch(`${API_URL}/api/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: field_username.value, password: password.value })
  });
  const data = await r.json();
  if (r.status !== 201) alert(data.error || 'Rejestracja nieudana');
  else {
    alert('Rejestracja udana! Zaloguj się.');
    register_visible.value = false;
  }
}

async function login() {
  const r = await fetch(`${API_URL}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: field_username.value, password: password.value })
  });
  const data = await r.json();
  if (r.status !== 200) {
    alert(data.error || 'Logowanie nieudane');
    return;
  }

  //zapisanie tokenu i nazwy urzytkownika 
  localStorage.setItem('token', data.token);
  localStorage.setItem('username', data.user.username);

  emit("updateUsername", field_username.value)
  emit("updateIsLogged", true)
}
</script>

<template>
  <section id="auth-section">
    <h2>Logowanie</h2>
    <form id="login-form" class="row">
      <input v-model="field_username" type="text" id="login-username" placeholder="Nazwa użytkownika" required />
      <input v-model="password" type="password" id="login-password" placeholder="Hasło" required />
      <button type="submit" @click.prevent="login()">Zaloguj</button>
    </form>

    <p class="muted">Nie masz konta? <a href="#" @click.prevent="register_visible = true" id="show-register">Zarejestruj
        się</a></p>

    <div v-if="register_visible" id="register-section">
      <h2>Rejestracja</h2>
      <form id="register-form" class="row">
        <input v-model="field_username" type="text" id="reg-username" placeholder="Nazwa użytkownika" required />
        <input v-model="password" type="password" id="reg-password" placeholder="Hasło" required />
        <button type="submit" @click.prevent="register()">Zarejestruj</button>
      </form>
    </div>

  </section>

</template>

<style scoped></style>