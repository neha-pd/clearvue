import { ref, watch, nextTick, onBeforeUnmount, useId } from '../vendor/vue.esm-browser.prod.js';

/** Small, browser-first Vue primitives. Public props/events are documented in README. */
export const CvButton = {
  props: { variant: { default: 'primary' }, disabled: Boolean, type: { default: 'button' } },
  template: `<button :type="type" :disabled="disabled" class="cv-button" :class="'cv-button--'+variant"><slot /></button>`
};
export const CvTextInput = {
  inheritAttrs: false,
  props: { modelValue: { default: '' }, label: { type: String, required: true }, hint: String, error: String, id: String, required: Boolean, type: { default: 'text' } },
  emits: ['update:modelValue'],
  setup(props) { const uid = props.id || 'cv-input-'+useId(); return { uid }; },
  template: `<div class="cv-field"><label :for="uid">{{label}} <span v-if="required" class="required">(required)</span></label><p v-if="hint" :id="uid+'-hint'" class="cv-hint">{{hint}}</p><input v-bind="$attrs" :id="uid" :type="type" :value="modelValue" :required="required" :aria-invalid="error ? 'true' : undefined" :aria-describedby="[hint ? uid+'-hint' : '', error ? uid+'-error' : ''].filter(Boolean).join(' ') || undefined" @input="$emit('update:modelValue', $event.target.value)"><p v-if="error" :id="uid+'-error'" class="cv-error">{{error}}</p></div>`
};
export const CvAlert = {
  props: { tone: { default: 'info' }, title: String, urgent: Boolean },
  template: `<div class="cv-alert" :class="'cv-alert--'+tone" :role="urgent ? 'alert' : 'status'" aria-atomic="true"><strong v-if="title">{{title}}</strong><div><slot /></div></div>`
};
export const CvDisclosure = {
  props: { label: { type: String, required: true }, initiallyOpen: Boolean },
  setup(props) { return { open: ref(props.initiallyOpen), uid: 'cv-disclosure-'+useId() }; },
  template: `<div class="cv-disclosure"><button type="button" :aria-expanded="open" :aria-controls="uid" @click="open=!open">{{label}} <span aria-hidden="true">{{open ? '−' : '+'}}</span></button><div v-show="open" :id="uid" class="cv-disclosure-content"><slot /></div></div>`
};
export const CvDialog = {
  props: { modelValue: Boolean, title: { type: String, required: true }, description: String },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const el = ref(null), uid = 'cv-dialog-'+useId(); let trigger;
    const close = () => emit('update:modelValue', false);
    watch(() => props.modelValue, async (open) => {
      await nextTick(); if (!el.value) return;
      if (open && !el.value.open) { trigger = document.activeElement; el.value.showModal(); }
      else if (!open && el.value.open) { el.value.close(); if (trigger?.isConnected) trigger.focus(); }
    }, { immediate: true });
    onBeforeUnmount(() => { if (el.value?.open) el.value.close(); if (trigger?.isConnected) trigger.focus(); });
    function containTab(event) {
      if (event.key !== 'Tab') return;
      const items = [...el.value.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])')].filter(node => node.getClientRects().length);
      const first=items[0], last=items.at(-1);
      if (!first) { event.preventDefault(); return; }
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    return { el, uid, close, containTab };
  },
  template: `<dialog ref="el" class="cv-dialog" :aria-labelledby="uid+'-title'" :aria-describedby="description ? uid+'-description' : undefined" @cancel.prevent="close" @close="close" @keydown="containTab"><h2 :id="uid+'-title'">{{title}}</h2><p v-if="description" :id="uid+'-description'">{{description}}</p><slot :close="close" /><button class="cv-dialog-close" type="button" autofocus @click="close">Close dialog</button></dialog>`
};
export const CvTabs = {
  props: { tabs: { type: Array, required: true }, label: { type: String, required: true } },
  setup(props) {
    const active = ref(0), uid = 'cv-tabs-'+useId(), root = ref(null);
    function keydown(e, index) {
      let target;
      if (e.key === 'ArrowRight') target = (index+1) % props.tabs.length;
      if (e.key === 'ArrowLeft') target = (index-1+props.tabs.length) % props.tabs.length;
      if (e.key === 'Home') target = 0;
      if (e.key === 'End') target = props.tabs.length-1;
      if (target !== undefined) { e.preventDefault(); active.value=target; nextTick(() => root.value.querySelectorAll('[role="tab"]')[target].focus()); }
    }
    return { active, uid, root, keydown };
  },
  template: `<div class="cv-tabs" ref="root"><div role="tablist" :aria-label="label"><button v-for="(tab,i) in tabs" :key="tab.id" type="button" role="tab" :id="uid+'-tab-'+i" :aria-controls="uid+'-panel-'+i" :aria-selected="active===i" :tabindex="active===i ? 0 : -1" @click="active=i" @keydown="keydown($event,i)">{{tab.label}}</button></div><div v-for="(tab,i) in tabs" :key="tab.id" v-show="active===i" role="tabpanel" tabindex="0" :id="uid+'-panel-'+i" :aria-labelledby="uid+'-tab-'+i"><slot :name="tab.id">{{tab.content}}</slot></div></div>`
};
