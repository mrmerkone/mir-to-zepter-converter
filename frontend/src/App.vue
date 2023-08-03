<template>
  <div class="container d-flex justify-content-center">
    <div class="card vertical-center">
      <div class="card-body">
        <form class="row g-3">
          <div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" @change="calculate" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="USD" v-model="currency" checked>
              <label class="form-check-label" for="inlineRadio1">$ по {{discounted.USD}}</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" @change="calculate" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="EUR" v-model="currency">
              <label class="form-check-label" for="inlineRadio2">€ по {{discounted.EUR}}</label>
            </div>
          </div>
          <div>
            <input v-model="requiredAmount" @input="calculate" @keypress="isNumber($event)" class="form-control" type="text" placeholder="Сколько нужно в валюте">
          </div>
          <div class="card-text" v-if="transferAmount">
            <p><b>{{transferAmount}} руб.</b> нужно перевести<br> <b>{{this.instantDepositingAmount}} {{this.currencySign}}</b> придет сразу <br> <b>{{this.deferredDepositingAmount}} {{this.currencySign}}</b> через пару дней</p>
          </div>
        </form>
      </div>
    </div>
  </div>
  <div class="footer">
    <div class="container text-center">
      <p>Баги и предложения <a href="https://github.com/mrmerkone/mir-to-zepter-converter/issues/new">сюда</a>.</p>
    </div>
  </div>
</template>
<script>
import axios from 'axios';

const CURRENCY_SIGN_MAP = {
  "EUR": "€",
  "USD": "$",
}
    
export default {
  data() {
    return {
      discounted: {"EUR": "???", "USD": "???"},
      full: {"EUR": "???", "USD": "???"},
      currency: "USD",
      requiredAmount: "",
      transferAmount: "",
      instantDepositingAmount: "",
      deferredDepositingAmount: "",
    }
  },
  computed: {
    currencySign: function () {
      return CURRENCY_SIGN_MAP[this.currency]
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
      let requiredAmount = parseFloat(this.requiredAmount);
      this.transferAmount = Math.round((requiredAmount * this.discounted[this.currency]) * 100) / 100;
      this.instantDepositingAmount = Math.round((this.transferAmount / this.full[this.currency]) * 100) / 100;
      this.deferredDepositingAmount = Math.round((requiredAmount - this.instantDepositingAmount) * 100) / 100;
    }
  },
  mounted() {
    axios
      .get('api/rates')
      .then(
        response => {
          this.discounted = response.data.discounted;
          this.full = response.data.full;
        }
      );
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
.footer {
    margin: 0 1rem;
    position: absolute;
    top: 99%;
    left: 50%;
    font-size: 0.6em;
    transform: translateY(-50%) translateX(-50%);
}
</style>
