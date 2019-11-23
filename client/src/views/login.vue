<template>
  <div class="container">
    <form @submit="onSubmit">
      <div class="form-group">
        <label>Username:</label>
        <input
          class="form-control"
          type="text"
          name="username"
          v-model="input.username"
          placeholder="Username"
        />
      </div>
      <div class="form-group">
        <label>Password:</label>
        <input
          class="form-control"
          type="password"
          name="password"
          v-model="input.password"
          placeholder="Password"
        />
      </div>
      <button type="submit" class="btn btn-primary" variant="primary">Submit</button>
      <div class="form-group">
        <label>{{ message }}</label>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Login",
  data() {
    return {
      message: "",
      input: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    login() {
      if (this.input.username != "" && this.input.password != "") {
        const path = "http://localhost:5000/authentication";
        const payload = {
          username: this.input.username,
          password: this.input.password
        };
        function enviarLogin(path, payload, callback) {
          axios
            .post(path, payload)
            .then(response => {
              callback(response.data.login);
            })
            .catch(error => {
              console.log(error);
            });
        }
        const self = this;
        enviarLogin(path, payload, function(response) {
          if (response == "success") {
            self.$emit("authenticated", true);
            self.$router.replace({ name: "grafica" });
          } else {
            self.message = "The username and / or password is incorrect";
          }
        });
      } else {
        this.message = "A username and password must be present";
      }
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.login();
    }
  }
};
</script>
