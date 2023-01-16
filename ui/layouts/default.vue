<script setup lang="ts">

</script>

<template>
    <div class="py-12">
        <header>
            <nav class="navbar bg-base-100 justify-center">
                <a class="btn btn-ghost normal-case text-xl">
                    <icon name="mdi:github" />
                </a>
            </nav>
        </header>
        <main class="m-auto max-w-xl">
            <slot></slot>
        </main>
    </div>
</template>
