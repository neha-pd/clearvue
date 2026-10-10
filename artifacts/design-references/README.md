# ClearVue redesign references

Researched before implementation on 11 October2026. Original implementation; reference art is not shipped on the public page.

- [Modern UI Component Library for Scalable Design Systems, reloadux](https://dribbble.com/shots/26154629-Modern-UI-Component-Library-for-Scalable-Design-Systems): actual component overview and typography specimen inspected in browser. Relevant ideas: a strong dark header, restrained green accents, clearly grouped controls, generous spacing around individual specimens. Adopt grouping and hierarchy, not screenshot artwork or copy.
- [Atomic Design UI Component Library, Ashwin K](https://www.behance.net/gallery/245827495/Design-System-Atomic-Design-UI-Component-Library): primary case-study text and module structure inspected; image panel did not finish loading in the captured browser viewport. Treat this as a written reference for foundations and categories, not a visually inspected full case study.
- [SaaS platform design system, Hanna Smarhunova](https://dribbble.com/shots/27679426-SaaS-platform-Design-system-and-component-library): primary indexed description distinguishes typography, tokens, components and developer handoff. Supports putting behavior notes and code beside a real live preview.

Design read: a developer interface lab, compact graphite navigation, cool porcelain workspace, restrained leaf-green accent, editorial sans typography. Dials variance6/motion2/density5. Native browser ESM Vue is retained; no unnecessary framework migration.

Substantive changes: move from a large marketing hero to a working library shell; group19 components into three browsable sections; add live search, explicit empty recovery, URL-linked component selection, wide/narrow preview and a copyable Vue code inspector. Preserve all component props/events and actual demos. Do not add fake usage counts, production claims or decorative dashboards. Native controls remain labeled; selected states have more than color; mobile navigation can scroll horizontally without page overflow. Honor stored theme and system preference on first visit.
