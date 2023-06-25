<template>
  <div class="container d-flex justify-content-center">
    <div class="card vertical-center">
      <div class="card-body">
        <form class="row g-3">
          <div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" @change="calculate" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="USD" v-model="currency" checked>
              <label class="form-check-label" for="inlineRadio1">$ по {{rates.USD}}</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" @change="calculate" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="EUR" v-model="currency">
              <label class="form-check-label" for="inlineRadio2">€ по {{rates.EUR}}</label>
            </div>
          </div>
          <div>
            <input v-model="amount" @input="calculate" @keypress="isNumber($event)" class="form-control" type="text" placeholder="Сколько нужно в валюте" aria-label="default input example">
          </div>
          <div v-if="transfer_amount">
            <p>Необходимо перевести <b>{{ transfer_amount }} руб.</b></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
export default {
  data() {
    return {
      rates: {"EUR": "???", "USD": "???"},
      currency: "USD",
      amount: "",
      transfer_amount: ""
    }
  },
  methods: {
    isNumber: function(event) {
      event = (event) ? event : window.event;
      var charCode = (event.which) ? event.which : event.keyCode;
      if ((charCode > 31 && (charCode < 48 || charCode > 57)) && charCode !== 46) {
        event.preventDefault();
      } else {
        return true;
      }
    },
    calculate: function () {
      let amount = parseFloat(this.amount);
      this.transfer_amount = amount * this.rates[this.currency];
      this.transfer_amount.toFixed(3);
    }
  },
  mounted() {
    axios
      .get('api/rates')
      .then(response => (this.rates = response.data));
  }
}
</script>
<style>
html, body {
    height: 100%;
}
.container {
    height: 100%;
}
.vertical-center {
    margin: 0 1rem;
    position: absolute;
    top: 30%;
    transform: translateY(-50%);
}
</style>
