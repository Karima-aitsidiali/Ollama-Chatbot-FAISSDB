<template>
  <div
    class="message-item"
    :class="{
      'user-message': isUser,
      'bot-message': !isUser,
      'error-message-bubble': message.isError
    }"
  >
    <div class="message-text" v-html="formattedText"></div>
    <!-- Section ressources supplémentaires, affichée dynamiquement -->
    <div
      v-if="showResources && message.resources && message.resources.length"
      class="resources-section"
    >
      <hr />
      <h4> Ressources Externes Supplémentaires  </h4>
      <ul>
        <li v-for="(res, idx) in message.resources" :key="idx">
          <a :href="res.url" target="_blank" rel="noopener">
            {{ res.title || res.url }}
          </a>
        </li>
      </ul>
    </div>
    <span class="message-timestamp">
      {{ new Date(message.timestamp).toLocaleTimeString() }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import markdownItKatex from 'markdown-it-katex'
import 'katex/dist/katex.min.css'

const props = defineProps({
  message: {
    type: Object,
    required: true,
  },
  showResources: {
    type: Boolean,
    default: false,
  },
})

const isUser = computed(() => props.message.sender === 'user')

// Configure MarkdownIt avec KaTeX pour le rendu LaTeX
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
}).use(markdownItKatex)

// Ajoute target="_blank" et rel="noopener" à tous les liens Markdown
const defaultRender = md.renderer.rules.link_open || function(tokens, idx, options, env, self) {
  return self.renderToken(tokens, idx, options)
}
md.renderer.rules.link_open = function(tokens, idx, options, env, self) {
  // Ajoute target="_blank"
  const aIndex = tokens[idx].attrIndex('target')
  if (aIndex < 0) {
    tokens[idx].attrPush(['target', '_blank'])
  } else {
    tokens[idx].attrs[aIndex][1] = '_blank'
  }
  // Ajoute rel="noopener"
  const relIndex = tokens[idx].attrIndex('rel')
  if (relIndex < 0) {
    tokens[idx].attrPush(['rel', 'noopener'])
  } else {
    tokens[idx].attrs[relIndex][1] = 'noopener'
  }
  return defaultRender(tokens, idx, options, env, self)
}

const formattedText = computed(() => {
  return md.render(props.message.text || '')
})
</script>

<style scoped>
@import 'katex/dist/katex.min.css';

.message-text {
  font-size: 1em;
  line-height: 1.6;
  color: inherit;
  word-break: break-word;
  overflow-wrap: break-word;
  max-width: 100%;
  margin: 0;
  padding: 0;
}

/* Titres */
.message-text h1,
.message-text h2,
.message-text h3 {
  font-weight: 700;
  margin: 0.7em 0 0.3em 0;
  color: #217dbb;
  line-height: 1.2;
}
.message-text h1 { font-size: 1.3em; }
.message-text h2 { font-size: 1.15em; }
.message-text h3 { font-size: 1.05em; }

/* Listes */
.message-text ul,
.message-text ol {
  margin: 0.5em 0 0.5em 1.5em;
  padding-left: 1.2em;
}
.message-text li {
  margin-bottom: 0.2em;
}
.message-item {
  margin-bottom: 18px;
  padding: 14px 18px;
  border-radius: 18px;
  max-width: 80%;
  width: fit-content;
  word-break: break-word;
  overflow-wrap: break-word;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  border: 1.5px solid #b3d8fd;           /* Contour bleu clair */
  box-shadow: 0 2px 8px rgba(52,152,219,0.08); /* Ombre subtile */
  background: #fff;                       /* Fond blanc pour contraste */
  transition: box-shadow 0.2s, border-color 0.2s;
}

/* Messages utilisateur (à droite, bleu) */
.user-message {
  background-color: #007bff;
  color: white;
  margin-left: auto;
  border-bottom-right-radius: 5px;
  border: 1.5px solid #217dbb;           /* Contour bleu plus foncé */
  box-shadow: 0 2px 12px rgba(33,125,187,0.13);
}

/* Messages bot (à gauche, gris clair) */
.bot-message {
  background-color: #f8fafc;
  color: #333;
  margin-right: auto;
  border-bottom-left-radius: 5px;
  border: 1.5px solid #b3d8fd;
  box-shadow: 0 2px 8px rgba(52,152,219,0.08);
}

/* Message d'erreur */
.error-message-bubble {
  background-color: #f8d7da;
  color: #721c24;
  border: 1.5px solid #f5c6cb;
  box-shadow: 0 2px 8px rgba(220,53,69,0.08);
}

/* Liens */
.message-text a {
  color: #217dbb;
  text-decoration: underline;
  transition: color 0.2s;
}
.message-text a:hover {
  color: #145a8a;
}

/* Citations */
.message-text blockquote {
  border-left: 4px solid #b3d8fd;
  background: #f4faff;
  color: #217dbb;
  margin: 0.7em 0;
  padding: 0.5em 1em;
  border-radius: 6px;
  font-style: italic;
}

/* Code inline */
.message-text code {
  background: #f4f4f4;
  color: #c7254e;
  padding: 2px 5px;
  border-radius: 4px;
  font-size: 0.97em;
}

/* Blocs de code */
.message-text pre {
  background: #f4f4f4;
  color: #333;
  padding: 10px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 0.7em 0;
  font-size: 0.97em;
  line-height: 1.4;
  word-break: break-word;
  white-space: pre-wrap;
  box-sizing: border-box;
}

/* Séparateurs */
.message-text hr {
  border: none;
  border-top: 1.5px solid #b3d8fd;
  margin: 1em 0;
}
</style>