<script setup lang="ts">
const transactions = ref({
  customer: [] as string[],
  date: [] as string[]
})
const newTransaction = ref({
  date: '',
  customer: ''
})

function addTransaction () {
  transactions.value.customer.push(newTransaction.value.customer)
  transactions.value.date.push(newTransaction.value.date)

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
  const result = await $fetch('http://localhost:5000/conditional-probability-alive', {
    headers: {
      'Content-Type': 'application/json'
    },
    method: 'POST',
    body: {
      transactions: transactions.value
    }
  })
  console.log(result)
}
</script>

<template>
  <div>
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
      <h2 class="font-bold">
        Agregar Transacciones
      </h2>
      <div class="flex flex-row gap-2">
        <div class="form-control basis-1/2">
          <label class="label">
            <span class="label-text">Fecha de la Transacción</span>
          </label>
          <input
            v-model="newTransaction.date"
            type="date"
            placeholder="Type here"
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
              <td>{{ new Date(transactions.date[i]).toLocaleDateString('es-VE') }}</td>
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
</template>
