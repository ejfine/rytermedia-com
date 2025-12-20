<script setup lang="ts">
type Image = {
  alt: string;
  src: string;
  category: "Family Portraits" | "Senior Athletes";
};

const { data: page } = await useAsyncData("gallery", () => {
  return queryCollection("gallery").first();
});
if (!page.value) {
  throw createError({
    statusCode: 404,
    statusMessage: "Page not found",
    fatal: true,
  });
}

const { global } = useAppConfig();
const groupedImages = computed((): Record<Image["category"], Image[]> => {
  const images = page.value?.images || [];
  const grouped: Record<Image["category"], Image[]> = {
    "Family Portraits": [],
    "Senior Athletes": [],
  };
  for (const image of images) {
    if (grouped[image.category]) grouped[image.category].push(image);
  }
  return grouped;
});
useSeoMeta({
  title: page.value?.seo?.title || page.value?.title,
  ogTitle: page.value?.seo?.title || page.value?.title,
  description: page.value?.seo?.description || page.value?.description,
  ogDescription: page.value?.seo?.description || page.value?.description,
});
</script>

<template>
  <UPage v-if="page">
    <UPageHero
      :title="page.title"
      :description="page.description"
      orientation="horizontal"
      :ui="{
        container: 'lg:flex sm:flex-row items-center',
        title: 'mx-0! text-left',
        description: 'mx-0! text-left',
        links: 'justify-start',
      }"
    />

    <UPageSection
      :ui="{
        container: 'pt-0!',
      }"
    >
      <div v-for="(imagesInCategory, category) in groupedImages" :key="category" class="mb-16 last:mb-0">
        <h2 class="text-2xl font-bold mb-4">
          <a :href="`#${category.toLowerCase().replace(/\s+/g, '-')}`">
            {{ category }}
          </a>
        </h2>
        <div>
          <div class="w-full" :class="{ 'masonry-container': imagesInCategory && imagesInCategory.length }">
            <ul v-if="imagesInCategory && imagesInCategory.length" class="grid grid-cols-1 gap-4 lg:block">
              <li
                v-for="image in imagesInCategory"
                ref="mansoryItem"
                :key="image.src"
                class="relative w-full group masonry-item"
              >
                <UModal fullscreen :title="image.alt">
                  <img
                    :src="image.src"
                    width="527"
                    height="430"
                    class="cursor-pointer h-auto w-full max-h-[430px] rounded-md transition-all duration-200 border-image brightness-[.8] hover:brightness-100 will-change-[filter] object-cover"
                    loading="lazy"
                  />
                  <template #body>
                    <img :src="image.src" width="100%" loading="lazy" />
                  </template>
                </UModal>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </UPageSection>
  </UPage>
</template>

<style scoped lang="postcss">
@media (min-width: 768px) {
  .imageEl {
    view-transition-name: vtn-image;
  }

  .bottom-menu-description {
    view-transition-name: vtn-bottom-menu-description;
  }

  .bottom-menu-button {
    view-transition-name: vtn-bottom-menu-button;
  }

  .container-image {
    background-color: rgba(255, 255, 255, 0.1);
  }

  .container-image:hover {
    background-color: transparent;
  }

  .border-image {
    border-width: 1.15px;
    border-color: rgba(255, 255, 255, 0.1);
  }
}

@media screen and (min-width: 1024px) {
  .masonry-container {
    column-count: 3;
    column-gap: 20px;
    column-fill: balance;
    margin: 20px auto 0;
    padding: 2rem;
  }

  .masonry-item,
  .upload {
    display: inline-block;
    margin: 0 0 20px;
    -webkit-column-break-inside: avoid;
    page-break-inside: avoid;
    break-inside: avoid;
    width: 100%;
  }
}
</style>
