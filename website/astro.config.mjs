// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import rehypeMarkdownLinks from './src/rehype-markdown-links.js';
import rehypeBasePaths from './src/rehype-base-paths.js';
import { getSiteUrl } from './src/lib/site-url.mjs';
import { locales } from './src/lib/locales.mjs';

const siteUrl = getSiteUrl();
const urlParts = new URL(siteUrl);
// Normalize basePath: ensure trailing slash so links can use `${BASE_URL}path`
const basePath = urlParts.pathname === '/' ? '/' : urlParts.pathname.endsWith('/') ? urlParts.pathname : urlParts.pathname + '/';

export default defineConfig({
  site: `${urlParts.origin}${basePath}`,
  base: basePath,
  outDir: '../build/site',

  // Disable aggressive caching in dev mode
  vite: {
    optimizeDeps: {
      force: true, // Always re-bundle dependencies
    },
    server: {
      watch: {
        usePolling: false, // Set to true if file changes aren't detected
      },
    },
  },

  markdown: {
    rehypePlugins: [
      [rehypeMarkdownLinks, { base: basePath }],
      [rehypeBasePaths, { base: basePath }],
    ],
  },

  integrations: [
    sitemap(),
    starlight({
      title: 'BMad Builder',
      tagline: 'Tool for creating custom BMad agents and modules.',

      // i18n: locale config from shared module (website/src/lib/locales.mjs)
      defaultLocale: 'root',
      locales,

      favicon: '/favicon.ico',

      // Social links
      social: [
        { icon: 'discord', label: 'Discord', href: 'https://discord.gg/gk8jAdXWmj' },
        { icon: 'github', label: 'GitHub', href: 'https://github.com/bmad-code-org/bmad-builder' },
        { icon: 'youtube', label: 'YouTube', href: 'https://www.youtube.com/@BMadCode' },
      ],

      // Show last updated timestamps
      lastUpdated: true,

      // Custom head tags for LLM discovery
      head: [
        {
          tag: 'meta',
          attrs: {
            name: 'ai-terms',
            content: `AI-optimized documentation: ${siteUrl}/llms-full.txt (plain text). Index: ${siteUrl}/llms.txt`,
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'llms-full',
            content: `${siteUrl}/llms-full.txt`,
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'llms',
            content: `${siteUrl}/llms.txt`,
          },
        },
      ],

      // Custom CSS
      customCss: ['./src/styles/custom.css'],

      // Sidebar configuration (Diataxis structure)
      sidebar: [
        {
          label: 'Welcome',
          translations: { 'zh-CN': '欢迎' },
          slug: 'index',
        },
        {
          label: 'Tutorials',
          translations: { 'zh-CN': '教程' },
          collapsed: false,
          autogenerate: { directory: 'tutorials' },
        },
        {
          label: 'How-To Guides',
          translations: { 'zh-CN': '操作指南' },
          collapsed: true,
          autogenerate: { directory: 'how-to' },
        },
        {
          label: 'Explanation',
          translations: { 'zh-CN': '概念说明' },
          collapsed: true,
          autogenerate: { directory: 'explanation' },
        },
        {
          label: 'Reference',
          translations: { 'zh-CN': '参考' },
          collapsed: true,
          autogenerate: { directory: 'reference' },
        },
        {
          label: 'BMad Ecosystem',
          translations: { 'zh-CN': 'BMad 生态' },
          collapsed: false,
          items: [
            { label: 'BMad Method', translations: { 'zh-CN': 'BMad 方法' }, link: 'https://docs.bmad-method.org/', attrs: { target: '_blank' } },
            { label: 'Creative Intelligence Suite', translations: { 'zh-CN': '创意智能套件' }, link: 'https://cis-docs.bmad-method.org/', attrs: { target: '_blank' } },
            { label: 'Game Dev Studio', translations: { 'zh-CN': '游戏开发工作室' }, link: 'https://game-dev-studio-docs.bmad-method.org/', attrs: { target: '_blank' } },
            { label: 'Test Architect (TEA)', translations: { 'zh-CN': '测试架构师 (TEA)' }, link: 'https://bmad-code-org.github.io/bmad-method-test-architecture-enterprise/', attrs: { target: '_blank' } },
          ],
        },
      ],

      // Credits in footer
      credits: false,

      // Pagination
      pagination: false,

      // Use our docs/404.md instead of Starlight's built-in 404
      disable404Route: true,

      // Custom components
      components: {
        Header: './src/components/Header.astro',
        MobileMenuFooter: './src/components/MobileMenuFooter.astro',
      },

      // Table of contents
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
    }),
  ],
});
