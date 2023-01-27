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
    transactions.value.customer.splice(id, id)
    transactions.value.date.splice(id, id)
  }
}

async function predict () {
  const response = await $fetch(`${runtimeConfig.apiUrl}/conditional-probability-alive`, {
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
  }
}
</script>

<template>
  <div>
    <div class="m-auto max-w-xl">
      <h1 class="text-center font-bold text-lg pb-6">
        DESARROLLO DE UN SISTEMA PARA INFERIR LA DESERCIÓN DE LOS
        CLIENTES EN UN E-COMMERCE
      </h1>

      <p class="text-base pb-6">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Commodi obcaecati, nihil aspernatur, laboriosam
        reiciendis velit reprehenderit sapiente provident saepe ullam magnam dolor voluptatibus illo minus quod, libero
        accusantium esse incidunt!
      </p>

      <form class="pb-6" @submit.prevent="addTransaction">
        <h2 class="font-bold text-xl">
          Agregar Transacciones
        </h2>
        <div class="flex flex-row gap-2">
          <div class="form-control basis-1/2">
            <label class="label">
              <span class="label-text">Fecha de la Transacción</span>
            </label>
            <input
              v-model="newTransaction.date"
              type="text"
              placeholder="DD-MM-YYYY"
              class="input input-bordered w-full max-w-xs"
            >
            <label class="label">
              <span class="label-text-alt">Alt label</span>
            </label>
          </div>
          <div class="form-control basis-1/2">
            <label class="label">
              <span class="label-text">Identificador de Cliente</span>
            </label>
            <input
              v-model="newTransaction.customer"
              type="text"
              placeholder="Type here"
              class="input input-bordered w-full max-w-xs"
            >
            <label class="label">
              <span class="label-text-alt">Alt label</span>
            </label>
          </div>
        </div>
        <div class="flex justify-end">
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
      <div v-for="(value, name) in result" :key="name">
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
                label: 'Probabilidad de Desertar',
                spanGaps: true,
                pointRadius: 0
              }
            ]
          }"
        />
      </div>
    </div>
  </div>
</template>
