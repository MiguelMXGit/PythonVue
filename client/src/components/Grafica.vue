<template>
  <div class="container">
    <form @submit="onSubmit">
        <div class="form-group">
            <label>X List:</label>
            <input class="form-control" id="form-listX" v-model="listas.listaX" >
        </div>
        <div class="form-group">
            <label>Y List:</label>
            <input  class="form-control" id="form-listY" v-model="listas.listaY">
        </div>
        <button type="submit" class="btn btn-primary" variant="primary">Submit</button>    
    </form>
    <label>F(X):<pre>{{funcion}}</pre></label>
    <div class="w-100 p-3" style="height: 500px;" id="myDiv"></div>
  </div>
</template>

<script>
import axios from 'axios';
import Plotly from 'plotly.js'

export default {
  data() {
    return {
        puntosUsuario: null,
        puntosFuncion: null,
        funcion: null,
        exponentes: null,
        funcion_sin_exponentes: null,
        listas: { 
          listaX: '',
          listaY: '',
        }
    };
  },
  methods: {
    getGrafica() {
      const path = 'http://localhost:5000/grafica';
      axios.get(path)
        .then((res) => {
          this.puntosUsuario = res.data.puntosUsuario;
          this.puntosFuncion = res.data.puntosFuncion;
          this.funcion = res.data.funcion
          this.renderGrafica(this.puntosUsuario,this.puntosFuncion,this.funcion);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    enviarListas(payload){
      const path = 'http://localhost:5000/grafica';
      axios.post(path, payload)
        .then(() => {
          this.getGrafica();
        })
        .catch((error) => {
          console.log(error);
          this.getGrafica();
        });
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        listaX: this.listas.listaX,
        listaY: this.listas.listaY,
      }
      this.enviarListas(payload);
    },
    renderGrafica(userpoints,funcpoints,funcion) {
      if(funcion.includes('\n')){
        this.exponentes = funcion.split('\n')[0]
        this.funcion_sin_exponentes = funcion.split('\n')[1]
      }
      else 
      {
        this.funcion_sin_exponentes = funcion
      }
      
      //coordenadas del usuaio
      var uxcoord = [];
      var uycoord = [];
      //coordenadas del la funcion
      var fxcoord = [];
      var fycoord = [];

      userpoints.forEach(element => {
        uxcoord.push(element.X);
        uycoord.push(element.Y);
      });

       funcpoints.forEach(element => {
        fxcoord.push(element.X);
        fycoord.push(element.Y);
      });

      var user_line = {
        x: uxcoord,
        y: uycoord,
        type: 'scatter',
        name: 'User Points'
      };

      var func_line = {
        x: fxcoord,
        y: fycoord,
        type: 'scatter',
        name: 'F(X)'
      };

      var data = [user_line,func_line];
      
      Plotly.newPlot('myDiv', data, {responsive: true});
    },
  },
  created() {
    this.getGrafica();
  },
};
</script>