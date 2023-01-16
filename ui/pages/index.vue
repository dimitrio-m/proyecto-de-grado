<script setup lang="ts">

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

      <form action="" class="pb-6">
         <h2 class="font-bold">Agregar Transacciones</h2>
         <div class="flex flex-row gap-2">
            <div class="form-control basis-1/2">
               <label class="label">
                  <span class="label-text">Fecha de la Transacción</span>
               </label>
               <input type="date" placeholder="Type here" class="input input-bordered w-full max-w-xs" />
               <label class="label">
                  <span class="label-text-alt">Alt label</span>
               </label>
            </div>
            <div class="form-control basis-1/2">
               <label class="label">
                  <span class="label-text">Identificador de Cliente</span>
               </label>
               <input type="text" placeholder="Type here" class="input input-bordered w-full max-w-xs" />
               <label class="label">
                  <span class="label-text-alt">Alt label</span>
               </label>
            </div>
         </div>
         <div class="flex justify-end">
            <button class="btn btn-primary">Registrar</button>
         </div>
      </form>
      <div>
         <div class="overflow-x-auto">
            <table class="table w-full">
               <!-- head -->
               <thead>
                  <tr>
                     <th></th>
                     <th>Fecha</th>
                     <th>Cliente</th>
                     <th></th>
                  </tr>
               </thead>
               <tbody>
                  <!-- row 1 -->
                  <tr>
                     <th>1</th>
                     <td>{{ new Date().toLocaleDateString('es-VE') }}</td>
                     <td>C9718382</td>
                     <td> <button class="btn btn-error btn-xs">eliminar</button></td>
                  </tr>
               </tbody>
            </table>
         </div>
         <div class="flex justify-end mt-6">
            <button class="btn btn-primary">Predecir</button>
         </div>
      </div>
   </div>
</template>
