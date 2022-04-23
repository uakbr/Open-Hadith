<script>
	import '../styles/tailwind-output.css';
	import Nav from '$lib/Nav.svelte';
</script>

<Nav />

<slot />

<div class="flex flex-col gap-1 mt-8 mb-8">
	<p class="text-xs font-medium text-center text-gray-500">
		Built with ❤️ by
		<a href="https://github.com/uakbr" class="text-gray-500 hover:underline">Anonymous </a>
	</p>
	<p class="text-xs text-center text-gray-500">
		© 2022
		<span class="mx-1">|</span>
		<a href="https://github.com/uakbr/open-hadith" class="text-gray-500 hover:underline"
			>Open Hadith
		</a>
	</p>
</div>
