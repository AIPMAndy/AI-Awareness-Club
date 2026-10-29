/* AI Awareness Club: no trackers, no external API calls, no server storage. */
(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const STORAGE_PREFIX = 'ai-awareness-club:v1:';
  const read = (key, fallback) => {
    try { const value = localStorage.getItem(STORAGE_PREFIX + key); return value === null ? fallback : JSON.parse(value); }
    catch { return fallback; }
  };
  const write = (key, value) => { try { localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value)); } catch { /* storage can be unavailable */ } };

  const themeToggle = $('.theme-toggle');
  const savedTheme = read('theme', null);
  if (savedTheme === 'dark' || savedTheme === 'light') document.documentElement.dataset.theme = savedTheme;
  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    write('theme', next);
  });

  const menuButton = $('.menu-button');
  const mobileNav = $('#mobile-nav');
  menuButton?.addEventListener('click', () => {
    const opened = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!opened));
    menuButton.setAttribute('aria-label', opened ? '打开菜单' : '关闭菜单');
    mobileNav.hidden = opened;
  });
  $$('#mobile-nav a').forEach(a => a.addEventListener('click', () => { mobileNav.hidden = true; menuButton?.setAttribute('aria-expanded', 'false'); }));

  const paths = {
    starter: ['七天完成第一份 AI 作品', '从一个你真实需要解决的任务开始，留下七份成果。', 'ai-first-week'],
    career: ['五步准备 AI 转型证据', '岗位研究、真实项目、能力补缺、投递记录、模拟面试。', 'career-transition'],
    business: ['验证第一个真实付费需求', '先访谈客户，写出服务交付边界，验证有人愿意买单。', 'first-customer'],
    leader: ['建立一份可验收的 AI 试点', '从业务问题开始，计算真实成本，设立质量和安全关口。', 'executive-ai']
  };
  $$('.path-choice').forEach(button => button.addEventListener('click', () => {
    const route = paths[button.dataset.path];
    if (!route) return;
    $$('.path-choice').forEach(other => { other.classList.toggle('is-active', other === button); other.setAttribute('aria-pressed', String(other === button)); });
    $('#path-title').textContent = route[0];
    $('#path-description').textContent = route[1];
    const prefix = document.documentElement.dataset.siteRoot || './';
    $('#path-link').href = new URL(prefix + 'guides/' + route[2] + '/index.html', document.baseURI).href;
  }));

  const search = $('#guide-search');
  const categoryFilter = $('#category-filter');
  if (search && categoryFilter) {
    const updateFilter = () => {
      const query = search.value.trim().toLocaleLowerCase();
      const category = categoryFilter.value;
      let count = 0;
      $$('[data-filter-item]').forEach(card => {
        const ok = (category === 'all' || card.dataset.category === category) && (card.dataset.keywords || '').toLocaleLowerCase().includes(query);
        card.hidden = !ok;
        if (ok) count++;
      });
      $('#result-count').textContent = `共 ${count} 条指南`;
      $('#no-results').hidden = count !== 0;
    };
    search.addEventListener('input', updateFilter);
    categoryFilter.addEventListener('change', updateFilter);
  }

  const checks = $$('input[data-step][data-guide]');
  if (checks.length) {
    const slug = checks[0].dataset.guide;
    const storageKey = 'progress:' + slug;
    const saved = read(storageKey, {});
    checks.forEach(box => {
      box.checked = !!saved[box.dataset.step];
      box.addEventListener('change', () => { update(); });
    });
    function update() {
      const result = {};
      checks.forEach(box => { result[box.dataset.step] = box.checked; box.closest('.step-card')?.classList.toggle('is-complete', box.checked); });
      write(storageKey, result);
      const done = checks.filter(box => box.checked).length;
      $('#progress-status').textContent = `${done} / ${checks.length} 已完成`;
      $('#progress-bar').style.width = Math.round(done / checks.length * 100) + '%';
    }
    update();
    $('#reset-progress')?.addEventListener('click', () => {
      if (!window.confirm('确定清空本页的学习进度吗？')) return;
      checks.forEach(box => { box.checked = false; });
      update();
    });
    $('#export-progress')?.addEventListener('click', () => {
      const name = document.querySelector('h1')?.textContent?.trim() || '学习进度';
      const text = [name, 'AI醒觉社 · 个人学习记录', '导出日期：' + new Date().toISOString().slice(0, 10), '', ...checks.map(box => `${box.checked ? '[x]' : '[ ]'} ${box.closest('.step-card')?.querySelector('h3')?.textContent?.trim() || '步骤'}`), '', '仅供个人记录，不代表认证。'].join('\n');
      const blob = new Blob([text], {type: 'text/plain;charset=utf-8'});
      const objectUrl = URL.createObjectURL(blob);
      const a = document.createElement('a'); a.href = objectUrl; a.download = `AI-Awareness-Club-${slug}-progress.txt`; a.click();
      setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
    });
  }
})();
