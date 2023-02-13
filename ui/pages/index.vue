<script setup lang="ts">
import { LineChart } from 'vue-chart-3'
import moment from 'moment'

const runtimeConfig = useRuntimeConfig()
const transactions = ref({
  customer: [] as string[],
  date: [] as string[]
})
const newTransaction = ref({
  date: '',
  customer: ''
})
const formErrors = ref({
  date: false,
  client: false
})
const customerData = ref({} as {
   [k: string]: {
      startDate: string,
      transactions: string[]
   }
})
const result = ref({} as {
   [k: string]: {
      p_alive: number,
      dates: string[],
      path: number[]
      T: number,
      recency: number,
      frequency: number
   }
})

function generateDates (start: string, end: number) {
  const dateArray = []
  const currentDate = moment(start, 'DD-MM-YYYY').toDate()
  const endDate = new Date(currentDate).setDate(currentDate.getDate() + end)

  while (currentDate <= new Date(endDate)) {
    dateArray.push(moment(currentDate).format('DD-MM-YYYY'))
    // Use UTC date to prevent problems with time zones and DST
    currentDate.setUTCDate(currentDate.getUTCDate() + 1)
  }
  return dateArray
}

function addTransaction () {
  formErrors.value.date = false
  formErrors.value.client = false

  const utc = moment(newTransaction.value.date, 'DD-MM-YYYY', true)

  if (!utc.isValid()) {
    formErrors.value.date = true
  }

  if (!newTransaction.value.customer) {
    formErrors.value.client = true
  }

  if (formErrors.value.date || formErrors.value.client) {
    return false
  }

  transactions.value.customer.push(newTransaction.value.customer)
  transactions.value.date.push(moment(newTransaction.value.date, 'DD-MM-YYYY').format('DD-MM-YYYY'))

  if (!customerData.value[newTransaction.value.customer]) {
    customerData.value[newTransaction.value.customer] = {
      startDate: moment().format('DD-MM-YYYY'),
      transactions: []
    }
  }

  if (moment(customerData.value[newTransaction.value.customer].startDate, 'DD-MM-YYYY') > moment(newTransaction.value.date, 'DD-MM-YYYY')) {
    customerData.value[newTransaction.value.customer].startDate = moment(newTransaction.value.date, 'DD-MM-YYYY').format('DD-MM-YYYY')
  }

  customerData.value[newTransaction.value.customer].transactions.push(moment(newTransaction.value.date, 'DD-MM-YYYY').format('DD-MM-YYYY'))

  newTransaction.value = {
    date: '',
    customer: ''
  }
}

function removeTransaction (id: number) {
  if (id === 0) {
    transactions.value.customer.shift()
    transactions.value.date.shift()
  } else {
    transactions.value.customer.splice(id, 1)
    transactions.value.date.splice(id, 1)
  }
}

async function predict () {
  const response = await $fetch(`${runtimeConfig.public.apiBase}/conditional-probability-alive`, {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: {
      transactions: {
        customer: transactions.value.customer,
        date: transactions.value.date.map(e => moment(e, 'DD-MM-YYYY').format('MM/DD/YYYY'))
      }
    }
  }) as any
  result.value = response.result

  for (const customer in result.value) {
    const startDate = customerData.value[customer].startDate
    result.value[customer].dates = generateDates(startDate, 500)
    result.value[customer].path = result.value[customer].path.map(v => Math.floor((1 - v) * 1000) / 10)
  }
}

useHead({
  title: 'SISTEMA PARA INFERIR LA DESERCIÓN DE LOS CLIENTES EN UN E-COMMERCE'
})
</script>

<template>
  <div class="px-4">
    <div class="m-auto max-w-xl ">
      <h1 class="text-center font-bold text-xl pb-8">
        DESARROLLO DE UN SISTEMA PARA INFERIR LA DESERCIÓN DE LOS
        CLIENTES EN UN E-COMMERCE
      </h1>

      <p class="text-base pb-8 prose lg:prose-lg">
        Este sistema utiliza el modelo BG/NBD para inferir la deserción o churn de un cliente según sus transacciones. El modelo se ajustó utilizando <a class="underline text-primary" href="https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business"> de transacciones de ventas de una tienda de comercio electrónico con sede en el Reino Unido </a>.
      </p>

      <p class="text-base pb-10 prose lg:prose-lg">
        Para inferir la deserción de uno o varios clientes, es necesario saber las transacciones que realizaron, por favor registre las transacciones mediante el siguiente formulario:
      </p>

      <form class="pb-6" @submit.prevent="addTransaction">
        <h2 class="font-bold text-xl mb-2">
          Agregar Transacciones
        </h2>
        <div class="flex flex-col lg:flex-row gap-4">
          <div class="form-control lg:basis-1/2">
            <label class="label">
              <span class="label-text">Fecha de la Transacción</span>
            </label>
            <input
              v-model="newTransaction.date"
              type="text"
              placeholder="DD-MM-YYYY"
              class="input input-bordered w-full max-w-sm"
            >
            <label v-if="formErrors.date" class="label">
              <span class="label-text-alt text-error">Por favor ingrese una fecha válida en el formato DD-MM-YYYY, por ejemplo: 21-02-2020</span>
            </label>
          </div>
          <div class="form-control lg:basis-1/2">
            <label class="label">
              <span class="label-text">Identificador de Cliente</span>
            </label>
            <input
              v-model="newTransaction.customer"
              type="text"
              placeholder="Type here"
              class="input input-bordered w-full max-w-sm"
            >
            <label v-if="formErrors.client" class="label">
              <span class="label-text-alt text-error">Por favor ingrese un identificador de cliente</span>
            </label>
          </div>
        </div>
        <div class="flex justify-end mt-6">
          <button type="submit" class="btn btn-primary">
            Registrar
          </button>
        </div>
      </form>
      <div v-if="transactions.customer.length">
        <div class="overflow-x-auto">
          <table class="table w-full">
            <thead>
              <tr>
                <th />
                <th>Fecha</th>
                <th>Cliente</th>
                <th />
              </tr>
            </thead>
            <tbody>
              <tr v-for="(customer, i) in transactions.customer" :key="i">
                <th>{{ i + 1 }}</th>
                <td>{{ transactions.date[i] }}</td>
                <td>{{ customer }}</td>
                <td class="text-right">
                  <button class="btn btn-error btn-xs" @click="removeTransaction(i)">
                    eliminar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="flex justify-end mt-6">
          <button type="button" class="btn btn-primary" @click.prevent="predict">
            Predecir
          </button>
        </div>
      </div>
    </div>
    <div v-if="Object.keys(result).length" class="m-auto max-w-5xl">
      <h2 class="font-bold text-xl pb-6">
        Resultados
      </h2>
      <div v-for="(value, name) in result" :key="name" class="pb-4">
        <h3 class="font-bold">
          Usuario: {{ name }}
        </h3>
        <LineChart
          class="w-full"
          :chart-data="{
            labels: value.dates,
            datasets: [
              {
                data: value.path,
                label: '% Probabilidad de haber desertado',
                spanGaps: true,
                pointRadius: 0,
                borderColor: 'rgba(200, 0, 0, 0.8)',
                backgroundColor: 'rgba(200, 0, 0, 0.2)',
              }
            ]
          }"
          :options="{
            scales: {
              y: {
                ticks: {
                  callback(value: number) {
                    return value + ' %';
                  }
                }
              }
            }
          }"
        />
      </div>
    </div>
  </div>
</template>
