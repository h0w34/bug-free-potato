<template>
<nav class="navbar navbar-expand-lg bg-body-tertiary p-3">
  <div class="container d-flex justify-content-center">
    <router-link class="navbar-brand col-2" to="/">Мои Утки🐥</router-link>

    <form class="container-fluid col-lg-6" role="search">
      <div class="input-group">
        <span class="input-group-text" id="basic-addon1">@</span>
        <input type="text" class="form-control" placeholder="Имя/дата/место" aria-label="Username" aria-describedby="basic-addon1">
      </div>
    </form>

    <div class="col-lg-4">
      <form class="container">
        <button class="btn btn-sm btn-outline-secondary me-2" type="button">Войти</button>
        <button class="btn btn-sm btn-outline-secondary" type="button">Зарегистрироваться</button>
      </form>
    </div>
  </div>
</nav>

</template>

<script>
export default {
  name: "Navbar-full"
}
</script>

<style scoped>

</style>