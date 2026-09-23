/**
 * Ohmly - Electronics eCommerce HTML Template
 * main.js  |  Version 1.0.0
 *
 * TABLE OF CONTENTS
 *  0. Settings (turn features on or off here)
 *  1. Helpers
 *  2. Preloader
 *  3. Sticky header
 *  4. Menus (dropdown toggles, mobile menu copy)
 *  5. Header search (small screens)
 *  6. Drawers and modals (mobile menu, mini-cart, filters, quick view)
 *  7. Quantity inputs
 *  8. Product gallery
 *  9. Variant select
 * 10. Price range filter
 * 11. Grid / list toggle
 * 12. Tabs
 * 13. Accordion
 * 14. Countdown timers
 * 15. Carousels
 * 16. Add to cart and wishlist feedback
 * 17. Cart page totals
 * 18. Form validation
 * 19. Newsletter popup
 * 20. Back to top
 */

/* ----------------------------------------------------------
   0. Settings
   Change true to false to switch a feature off site-wide.
---------------------------------------------------------- */
const SETTINGS = {
  preloader: true,          // loading screen on page load
  stickyHeader: true,       // header stays visible when scrolling
  newsletterPopup: true,    // shows once per visitor
  newsletterDelay: 5000,    // milliseconds before the popup appears
  quickView: true,          // "Quick view" modal on product cards
  backToTop: true,          // arrow button at bottom right
  countdown: true           // deal timers
};

(function () {
  "use strict";

  /* ----------------------------------------------------------
     1. Helpers
  ---------------------------------------------------------- */
  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select, textarea, [tabindex]:not([tabindex="-1"])';
  const money = (n) => "$" + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  const store = {
    get(key) { try { return window.localStorage.getItem(key); } catch (e) { return null; } },
    set(key, value) { try { window.localStorage.setItem(key, value); } catch (e) { /* storage unavailable */ } }
  };

  const toastRegion = $(".toast-region");
  function toast(message) {
    if (!toastRegion) return;
    const el = document.createElement("div");
    el.className = "toast";
    el.innerHTML = '<svg aria-hidden="true"><use href="#i-check"></use></svg><span></span>';
    el.querySelector("span").textContent = message;
    toastRegion.appendChild(el);
    setTimeout(() => { el.classList.add("is-leaving"); }, 2200);
    setTimeout(() => { el.remove(); }, 2600);
  }

  /* ----------------------------------------------------------
     2. Preloader
  ---------------------------------------------------------- */
  const preloader = $(".preloader");
  if (preloader) {
    if (!SETTINGS.preloader) {
      preloader.remove();
    } else {
      const hide = () => {
        preloader.classList.add("is-hidden");
        setTimeout(() => preloader.remove(), 400);
      };
      if (document.readyState === "complete") hide();
      else window.addEventListener("load", hide);
      setTimeout(hide, 3000); // never block the page for long
    }
  }

  /* ----------------------------------------------------------
     3. Sticky header
  ---------------------------------------------------------- */
  const header = $(".site-header");
  if (!SETTINGS.stickyHeader) {
    document.documentElement.classList.add("no-sticky");
  } else if (header) {
    const onScroll = () => header.classList.toggle("is-stuck", window.scrollY > 40);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ----------------------------------------------------------
     4. Menus
  ---------------------------------------------------------- */
  // Copy the desktop menu into the mobile drawer, so links are edited once per page
  const mainList = $(".main-nav .main-nav__list");
  const mobileNav = $(".mobile-nav");
  if (mainList && mobileNav) {
    const copy = mainList.cloneNode(true);
    $$("[id]", copy).forEach((el) => el.removeAttribute("id"));
    mobileNav.appendChild(copy);
  }

  // Dropdown / mega menu toggle buttons (touch and keyboard)
  document.addEventListener("click", (e) => {
    const toggle = e.target.closest(".submenu-toggle");
    if (toggle) {
      const item = toggle.closest(".main-nav__item");
      const open = !item.classList.contains("is-expanded");
      $$(".main-nav__item.is-expanded", item.parentElement).forEach((el) => {
        el.classList.remove("is-expanded");
        const btn = $(".submenu-toggle", el);
        if (btn) btn.setAttribute("aria-expanded", "false");
      });
      item.classList.toggle("is-expanded", open);
      toggle.setAttribute("aria-expanded", String(open));
      return;
    }
    // Close desktop menus when clicking elsewhere
    if (!e.target.closest(".main-nav")) {
      $$(".main-nav .main-nav__item.is-expanded").forEach((el) => {
        el.classList.remove("is-expanded");
        const btn = $(".submenu-toggle", el);
        if (btn) btn.setAttribute("aria-expanded", "false");
      });
    }
  });

  /* ----------------------------------------------------------
     5. Header search (small screens)
  ---------------------------------------------------------- */
  const searchToggle = $("[data-search-toggle]");
  const headerSearch = $(".site-header .header-search");
  if (searchToggle && headerSearch) {
    searchToggle.addEventListener("click", () => {
      const open = headerSearch.classList.toggle("is-open");
      searchToggle.setAttribute("aria-expanded", String(open));
      if (open) $("input", headerSearch).focus();
    });
  }

  /* ----------------------------------------------------------
     6. Drawers and modals
  ---------------------------------------------------------- */
  const overlay = $(".overlay");
  let activeLayer = null;
  let lastFocus = null;

  function openLayer(layer) {
    if (!layer) return;
    if (activeLayer) closeLayer(false);
    lastFocus = document.activeElement;
    layer.classList.add("is-open");
    if (overlay) overlay.classList.add("is-visible");
    document.body.classList.add("no-scroll");
    activeLayer = layer;
    const first = $(FOCUSABLE, layer);
    setTimeout(() => { if (first) first.focus(); }, 50);
  }

  function closeLayer(restoreFocus = true) {
    if (!activeLayer) return;
    const layer = activeLayer;
    layer.classList.remove("is-open");
    if (overlay) overlay.classList.remove("is-visible");
    document.body.classList.remove("no-scroll");
    activeLayer = null;
    layer.dispatchEvent(new CustomEvent("layer:close"));
    if (restoreFocus && lastFocus) lastFocus.focus();
  }

  // Quick view: fill the modal with the clicked card's details
  function fillQuickView(card) {
    const modal = $("#quick-view");
    if (!modal || !card) return;
    const img = $(".product-card__media img", card);
    const title = $(".product-card__title a", card);
    const price = $(".price", card);
    const specs = $(".spec-list", card);
    const target = {
      img: $("[data-qv-img]", modal),
      title: $("[data-qv-title]", modal),
      price: $("[data-qv-price]", modal),
      specs: $("[data-qv-specs]", modal),
      link: $("[data-qv-link]", modal)
    };
    if (img && target.img) { target.img.src = img.getAttribute("src"); target.img.alt = img.alt; target.img.toggleAttribute("data-photo", img.hasAttribute("data-photo")); }
    if (title && target.title) target.title.textContent = title.textContent;
    if (title && target.link) target.link.href = title.getAttribute("href");
    if (price && target.price) target.price.innerHTML = price.innerHTML;
    if (specs && target.specs) target.specs.innerHTML = specs.innerHTML;
  }

  if (!SETTINGS.quickView) document.documentElement.classList.add("no-quickview");

  document.addEventListener("click", (e) => {
    const cartBtn = e.target.closest("[data-open-cart]");
    if (cartBtn) { e.preventDefault(); openLayer($("#cart-drawer")); return; }

    const drawerBtn = e.target.closest("[data-open-drawer]");
    if (drawerBtn) { e.preventDefault(); openLayer(document.getElementById(drawerBtn.dataset.openDrawer)); return; }

    const qvBtn = e.target.closest("[data-quick-view]");
    if (qvBtn && SETTINGS.quickView) { fillQuickView(qvBtn.closest(".product-card")); openLayer($("#quick-view")); return; }

    const modalBtn = e.target.closest("[data-open-modal]");
    if (modalBtn) { e.preventDefault(); openLayer(document.getElementById(modalBtn.dataset.openModal)); return; }

    if (e.target.closest("[data-close]") || e.target === overlay) { closeLayer(); return; }
    if (activeLayer && activeLayer.classList.contains("modal") && e.target === activeLayer) closeLayer();
  });

  document.addEventListener("keydown", (e) => {
    if (!activeLayer) return;
    if (e.key === "Escape") { closeLayer(); return; }
    if (e.key === "Tab") { // keep focus inside the open layer
      const items = $$(FOCUSABLE, activeLayer).filter((el) => el.offsetParent !== null);
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Close the filters drawer if the screen grows past the sidebar breakpoint
  window.matchMedia("(min-width: 992px)").addEventListener("change", (mq) => {
    if (mq.matches && activeLayer && activeLayer.matches(".shop-sidebar:not(.shop-layout--full *), #mobile-menu")) closeLayer(false);
  });

  /* ----------------------------------------------------------
     7. Quantity inputs
  ---------------------------------------------------------- */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-qty-minus], [data-qty-plus]");
    if (!btn) return;
    const wrap = btn.closest("[data-qty]");
    if (!wrap) return;
    const input = $("input", wrap);
    const min = parseInt(input.min || "1", 10);
    const max = parseInt(input.max || "99", 10);
    let value = parseInt(input.value, 10) || min;
    value += btn.hasAttribute("data-qty-plus") ? 1 : -1;
    input.value = Math.min(max, Math.max(min, value));
    input.dispatchEvent(new Event("change", { bubbles: true }));
  });

  /* ----------------------------------------------------------
     8. Product gallery
  ---------------------------------------------------------- */
  $$("[data-gallery]").forEach((gallery) => {
    const main = $(".gallery__main img", gallery);
    const thumbs = $$("[data-src]", gallery);
    thumbs.forEach((thumb) => {
      thumb.addEventListener("click", () => {
        main.src = thumb.dataset.src;
        main.alt = thumb.dataset.alt || main.alt;
        thumbs.forEach((t) => t.setAttribute("aria-current", String(t === thumb)));
      });
    });
  });

  /* ----------------------------------------------------------
     9. Variant select
  ---------------------------------------------------------- */
  $$("[data-variant]").forEach((group) => {
    const output = $("[data-variant-value]", group);
    group.addEventListener("change", (e) => {
      if (output && e.target.matches("input")) output.textContent = e.target.value;
    });
  });

  /* ----------------------------------------------------------
     10. Price range filter
  ---------------------------------------------------------- */
  $$("[data-price-range]").forEach((range) => {
    const minInput = $(".range-min", range);
    const maxInput = $(".range-max", range);
    const minOut = $("[data-min-output]", range);
    const maxOut = $("[data-max-output]", range);
    const total = parseInt(maxInput.max, 10);
    const gap = 50;
    const update = (e) => {
      let lo = parseInt(minInput.value, 10);
      let hi = parseInt(maxInput.value, 10);
      if (hi - lo < gap) {
        if (e && e.target === minInput) { lo = hi - gap; minInput.value = lo; }
        else { hi = lo + gap; maxInput.value = hi; }
      }
      range.style.setProperty("--min", (lo / total) * 100 + "%");
      range.style.setProperty("--max", (hi / total) * 100 + "%");
      minOut.textContent = "$" + lo;
      maxOut.textContent = "$" + hi;
    };
    minInput.addEventListener("input", update);
    maxInput.addEventListener("input", update);
    update();
  });

  /* ----------------------------------------------------------
     11. Grid / list toggle
  ---------------------------------------------------------- */
  const grid = $("[data-product-grid]");
  $$("[data-view]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!grid) return;
      grid.classList.toggle("is-list", btn.dataset.view === "list");
      $$("[data-view]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
    });
  });

  /* ----------------------------------------------------------
     12. Tabs
  ---------------------------------------------------------- */
  $$("[data-tabs]").forEach((tabs) => {
    const list = $('[role="tablist"]', tabs);
    const tabItems = $$('[role="tab"]', list);
    const vertical = list.getAttribute("aria-orientation") === "vertical";
    const select = (tab, focus) => {
      tabItems.forEach((t) => {
        const selected = t === tab;
        t.setAttribute("aria-selected", String(selected));
        t.tabIndex = selected ? 0 : -1;
        const panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !selected;
      });
      if (focus) tab.focus();
    };
    tabItems.forEach((tab, i) => {
      tab.addEventListener("click", () => select(tab));
      tab.addEventListener("keydown", (e) => {
        const next = vertical ? "ArrowDown" : "ArrowRight";
        const prev = vertical ? "ArrowUp" : "ArrowLeft";
        let index = null;
        if (e.key === next) index = (i + 1) % tabItems.length;
        if (e.key === prev) index = (i - 1 + tabItems.length) % tabItems.length;
        if (e.key === "Home") index = 0;
        if (e.key === "End") index = tabItems.length - 1;
        if (index !== null) { e.preventDefault(); select(tabItems[index], true); }
      });
    });
    // Open a tab from a link, e.g. <a href="#reviews" data-tab-link>
    $$("[data-tab-link]").forEach((link) => {
      link.addEventListener("click", () => {
        const tab = tabItems.find((t) => t.getAttribute("aria-controls") === link.getAttribute("href").slice(1));
        if (tab) select(tab);
      });
    });
  });

  /* ----------------------------------------------------------
     13. Accordion
  ---------------------------------------------------------- */
  $$("[data-accordion]").forEach((acc) => {
    $$(".accordion__trigger", acc).forEach((trigger) => {
      trigger.addEventListener("click", () => {
        const open = trigger.getAttribute("aria-expanded") === "true";
        trigger.setAttribute("aria-expanded", String(!open));
        const panel = document.getElementById(trigger.getAttribute("aria-controls"));
        if (panel) panel.hidden = open;
      });
    });
  });

  /* ----------------------------------------------------------
     14. Countdown timers
     data-countdown="2026-12-31T23:59:59"  fixed end date
     data-countdown="+3d"                   rolling: 3 days from page load
  ---------------------------------------------------------- */
  const timers = $$("[data-countdown]");
  if (!SETTINGS.countdown) {
    timers.forEach((el) => el.remove());
  } else if (timers.length) {
    const units = [["days", 86400], ["hours", 3600], ["mins", 60], ["secs", 1]];
    timers.forEach((el) => {
      const value = el.dataset.countdown;
      const rolling = /^\+(\d+)d$/.exec(value);
      const end = rolling ? Date.now() + parseInt(rolling[1], 10) * 86400000 - 3723000 : new Date(value).getTime();
      el.textContent = "";
      el.setAttribute("role", "timer");
      const nums = units.map(([label]) => {
        const box = document.createElement("span");
        box.className = "countdown__unit";
        box.innerHTML = '<span class="countdown__num">00</span><span class="countdown__label">' + label + "</span>";
        el.appendChild(box);
        return $(".countdown__num", box);
      });
      const tick = () => {
        let left = Math.max(0, Math.floor((end - Date.now()) / 1000));
        if (left === 0) {
          el.textContent = el.dataset.endedText || "This deal has ended";
          el.classList.add("countdown--ended");
          clearInterval(id);
          return;
        }
        units.forEach(([, size], i) => {
          const n = Math.floor(left / size);
          left -= n * size;
          nums[i].textContent = String(n).padStart(2, "0");
        });
      };
      const id = setInterval(tick, 1000);
      tick();
    });
  }

  /* ----------------------------------------------------------
     15. Carousels
  ---------------------------------------------------------- */
  $$("[data-carousel]").forEach((carousel) => {
    const track = $(".carousel__track", carousel);
    const prev = $("[data-carousel-prev]", carousel);
    const next = $("[data-carousel-next]", carousel);
    const update = () => {
      if (prev) prev.disabled = track.scrollLeft <= 4;
      if (next) next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    };
    const move = (dir) => track.scrollBy({ left: dir * track.clientWidth * 0.8, behavior: "smooth" });
    if (prev) prev.addEventListener("click", () => move(-1));
    if (next) next.addEventListener("click", () => move(1));
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

  /* ----------------------------------------------------------
     16. Add to cart and wishlist feedback
     (visual only: connect to your store backend to save items)
  ---------------------------------------------------------- */
  const bump = (selector, delta) => {
    $$(selector).forEach((el) => { el.textContent = Math.max(0, (parseInt(el.textContent, 10) || 0) + delta); });
  };
  document.addEventListener("click", (e) => {
    const add = e.target.closest("[data-add-to-cart]");
    if (add) {
      e.preventDefault();
      const qtyInput = add.closest("form, .product-info, .quick-view") ? $("[data-qty] input", add.closest("form, .product-info, .quick-view")) : null;
      bump("[data-cart-count]", qtyInput ? parseInt(qtyInput.value, 10) || 1 : 1);
      const label = add.innerHTML;
      add.classList.add("is-added");
      add.textContent = "Added";
      setTimeout(() => { add.classList.remove("is-added"); add.innerHTML = label; }, 1400);
      toast("Added to cart");
      return;
    }
    const wish = e.target.closest("[data-wishlist]");
    if (wish) {
      e.preventDefault();
      const on = wish.getAttribute("aria-pressed") !== "true";
      wish.setAttribute("aria-pressed", String(on));
      bump("[data-wishlist-count]", on ? 1 : -1);
      toast(on ? "Saved to wishlist" : "Removed from wishlist");
    }
  });

  /* ----------------------------------------------------------
     17. Cart page totals
  ---------------------------------------------------------- */
  const cart = $("[data-cart-page]");
  if (cart) {
    const shippingFree = 99;
    const recalc = () => {
      let subtotal = 0;
      $$("tr[data-price]", cart).forEach((row) => {
        const qty = parseInt($("[data-qty] input", row).value, 10) || 1;
        const line = parseFloat(row.dataset.price) * qty;
        $("[data-line-total]", row).textContent = money(line);
        subtotal += line;
      });
      const shipping = subtotal === 0 || subtotal >= shippingFree ? 0 : 9.9;
      const set = (sel, text) => { const el = $(sel); if (el) el.textContent = text; };
      set("[data-subtotal]", money(subtotal));
      set("[data-shipping]", shipping ? money(shipping) : "Free");
      set("[data-total]", money(subtotal + shipping));
      if (!$$("tr[data-price]", cart).length) {
        const empty = $("[data-cart-empty]");
        cart.hidden = true;
        if (empty) empty.hidden = false;
      }
    };
    cart.addEventListener("change", recalc);
    cart.addEventListener("click", (e) => {
      const remove = e.target.closest("[data-remove-row]");
      if (!remove) return;
      remove.closest("tr").remove();
      bump("[data-cart-count]", -1);
      recalc();
    });
    recalc();
  }
  // Remove rows on wishlist and compare tables
  document.addEventListener("click", (e) => {
    const remove = e.target.closest("[data-remove-item]");
    if (!remove) return;
    const row = remove.closest("tr, .product-card");
    if (row) row.remove();
    if (remove.closest("[data-wishlist-page]")) bump("[data-wishlist-count]", -1);
  });

  /* ----------------------------------------------------------
     18. Form validation
     Add data-validate to a <form>. Add data-success="Message"
     to show a message instead of submitting (front-end demo).
  ---------------------------------------------------------- */
  $$("form[data-validate]").forEach((form) => {
    form.noValidate = true;
    const fields = $$("input, select, textarea", form).filter((f) => f.type !== "hidden" && f.type !== "submit");

    const showError = (field) => {
      const wrap = field.closest(".field") || field.parentElement;
      let msg = $(".field-error", wrap);
      const matchSel = field.dataset.match;
      let valid = field.checkValidity();
      if (valid && matchSel) {
        const other = $(matchSel, form);
        if (other && other.value !== field.value) valid = false;
      }
      if (valid) {
        field.removeAttribute("aria-invalid");
        if (msg) msg.remove();
        return true;
      }
      if (!msg) {
        msg = document.createElement("p");
        msg.className = "field-error";
        msg.id = (field.id || field.name || "field") + "-error";
        wrap.appendChild(msg);
      }
      field.setAttribute("aria-invalid", "true");
      field.setAttribute("aria-describedby", msg.id);
      if (matchSel && field.checkValidity()) msg.textContent = field.dataset.error || "The values do not match.";
      else if (field.validity.valueMissing) msg.textContent = field.dataset.error || "This field is required.";
      else if (field.validity.typeMismatch && field.type === "email") msg.textContent = "Enter a valid email address, like name@example.com.";
      else if (field.validity.tooShort) msg.textContent = "Use at least " + field.minLength + " characters.";
      else msg.textContent = field.dataset.error || field.validationMessage;
      return false;
    };

    fields.forEach((field) => {
      field.addEventListener("blur", () => { if (field.hasAttribute("aria-invalid") || field.value) showError(field); });
      field.addEventListener("input", () => { if (field.hasAttribute("aria-invalid")) showError(field); });
    });

    form.addEventListener("submit", (e) => {
      const invalid = fields.filter((f) => !showError(f));
      if (invalid.length) {
        e.preventDefault();
        invalid[0].focus();
        return;
      }
      if (form.dataset.success) {
        e.preventDefault();
        let note = $(".form-success", form.parentElement);
        if (!note) {
          note = document.createElement("p");
          note.className = "form-success";
          note.setAttribute("role", "status");
          form.insertAdjacentElement("afterend", note);
        }
        note.innerHTML = '<svg aria-hidden="true"><use href="#i-check"></use></svg><span></span>';
        note.querySelector("span").textContent = form.dataset.success;
        form.reset();
        if (form.closest("#newsletter-modal")) store.set("ohmly-newsletter", "done");
      }
    });
  });

  /* ----------------------------------------------------------
     19. Newsletter popup
  ---------------------------------------------------------- */
  const popup = $("#newsletter-modal");
  if (popup) {
    if (SETTINGS.newsletterPopup && !store.get("ohmly-newsletter")) {
      setTimeout(() => { if (!activeLayer) openLayer(popup); }, SETTINGS.newsletterDelay);
    }
    popup.addEventListener("layer:close", () => store.set("ohmly-newsletter", "done"));
  }

  /* ----------------------------------------------------------
     20. Back to top
  ---------------------------------------------------------- */
  const toTop = $(".back-to-top");
  if (toTop) {
    if (!SETTINGS.backToTop) {
      toTop.remove();
    } else {
      const onScroll = () => toTop.classList.toggle("is-visible", window.scrollY > 600);
      window.addEventListener("scroll", onScroll, { passive: true });
      toTop.addEventListener("click", () => window.scrollTo({ top: 0 }));
      onScroll();
    }
  }

  /* ----------------------------------------------------------
     21. Image fallback
     An image with data-fallback="path.svg" switches to that file if it
     cannot load (for example a remote demo photo that is offline).
  ---------------------------------------------------------- */
  const useFallback = (img) => {
    const alt = img.dataset.fallback;
    if (!alt) return;
    img.removeAttribute("data-fallback");
    img.removeAttribute("data-photo");
    img.src = alt;
  };
  document.addEventListener("error", (e) => { if (e.target.tagName === "IMG") useFallback(e.target); }, true);
  $$("img[data-fallback]").forEach((img) => { if (img.complete && img.naturalWidth === 0) useFallback(img); });
})();
