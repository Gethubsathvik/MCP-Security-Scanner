import { useState, useMemo } from 'react';
import {
  Leaf, Waves, Flower2, UtensilsCrossed, Car, Sparkles, Plus,
  TrendingDown, Wallet, CalendarDays, ChevronDown, Search, ArrowUpRight, ArrowDownRight
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, Tooltip, PieChart, Pie, Cell } from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const CATEGORIES = {
  stay:      { label: 'Villa & Stay',   icon: Leaf,            color: '#5C7460', soft: '#E8EFE6' },
  wellness:  { label: 'Spa & Healing',  icon: Flower2,         color: '#C77B53', soft: '#F8E9DF' },
  movement:  { label: 'Yoga & Movement',icon: Waves,           color: '#8A9A5B', soft: '#EFF2E2' },
  food:      { label: 'Nourishment',    icon: UtensilsCrossed, color: '#A86B3C', soft: '#F5EADC' },
  transport: { label: 'Getting Around', icon: Car,             color: '#6B7B8C', soft: '#E8EDF1' },
  ceremony:  { label: 'Ceremonies',     icon: Sparkles,        color: '#9C7A97', soft: '#F1E8F0' },
};

const TRANSACTIONS = [
  { id: 1,  name: 'Fivelements Retreat — riverside suite', cat: 'stay',      amount: 285.00, date: 'Oct 14', day: 'Mon', note: '3 of 7 nights' },
  { id: 2,  name: 'Sunrise vinyasa at The Yoga Barn',      cat: 'movement',  amount: 12.50,  date: 'Oct 14', day: 'Mon', note: 'Drop-in class' },
  { id: 3,  name: 'Balinese boreh body wrap',              cat: 'wellness',  amount: 48.00,  date: 'Oct 14', day: 'Mon', note: '90 min · Karsa Spa' },
  { id: 4,  name: 'Zest Ubud — jackfruit rendang bowl',    cat: 'food',      amount: 9.75,   date: 'Oct 14', day: 'Mon', note: 'Lunch' },
  { id: 5,  name: 'Scooter rental, week two',              cat: 'transport', amount: 38.00,  date: 'Oct 13', day: 'Sun', note: 'Honda Scoopy' },
  { id: 6,  name: 'Water purification at Tirta Empul',     cat: 'ceremony',  amount: 21.00,  date: 'Oct 13', day: 'Sun', note: 'Sarong + offering' },
  { id: 7,  name: 'Sayuri Healing Food — raw cacao cake',  cat: 'food',      amount: 6.20,   date: 'Oct 13', day: 'Sun', note: 'Afternoon treat' },
  { id: 8,  name: 'Sound bath at Pyramids of Chi',         cat: 'wellness',  amount: 32.00,  date: 'Oct 12', day: 'Sat', note: 'Evening session' },
  { id: 9,  name: 'Campuhan Ridge taxi, return',           cat: 'transport', amount: 7.40,   date: 'Oct 12', day: 'Sat', note: 'GoJek' },
  { id: 10, name: 'Breathwork intensive — Radiantly Alive',cat: 'movement',  amount: 28.00,  date: 'Oct 11', day: 'Fri', note: '2 hr workshop' },
  { id: 11, name: 'Moksa plant-based tasting menu',        cat: 'food',      amount: 34.50,  date: 'Oct 11', day: 'Fri', note: 'Dinner for one' },
  { id: 12, name: 'Melukat blessing with Ketut',           cat: 'ceremony',  amount: 45.00,  date: 'Oct 10', day: 'Thu', note: 'Private ceremony' },
];

const TREND = [
  { day: 'Oct 8',  amount: 96 },
  { day: 'Oct 9',  amount: 142 },
  { day: 'Oct 10', amount: 88 },
  { day: 'Oct 11', amount: 110 },
  { day: 'Oct 12', amount: 64 },
  { day: 'Oct 13', amount: 71 },
  { day: 'Oct 14', amount: 355 },
];

const BUDGET = 1850;

export default function App() {
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');

  const totalSpent = useMemo(() => TRANSACTIONS.reduce((s, t) => s + t.amount, 0) + 612.4, []);
  const remaining = BUDGET - totalSpent;
  const pct = Math.min((totalSpent / BUDGET) * 100, 100);

  const byCategory = useMemo(() => {
    const map = {};
    TRANSACTIONS.forEach(t => { map[t.cat] = (map[t.cat] || 0) + t.amount; });
    map.stay += 420; map.wellness += 96; map.food += 58.4; map.movement += 38;
    return Object.entries(map)
      .map(([key, value]) => ({ key, value, ...CATEGORIES[key] }))
      .sort((a, b) => b.value - a.value);
  }, []);

  const visible = TRANSACTIONS.filter(t =>
    (filter === 'all' || t.cat === filter) &&
    t.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-[#F7F3EC] text-[#2C2A24]" style={{ fontFamily: "'Karla', sans-serif" }}>
      <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Karla:wght@400;500;600;700&display=swap" rel="stylesheet" />
      <style dangerouslySetInnerHTML={{ __html: `
        .serif { font-family: 'Fraunces', serif; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #D6CDBE; border-radius: 99px; }
        .grain::before {
          content: ''; position: fixed; inset: 0; pointer-events: none; opacity: 0.035; z-index: 50;
          background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
        }
        .pill-fade { mask-image: linear-gradient(to right, black 92%, transparent); }
      `}} />
      <div className="grain" />

      <div className="max-w-6xl mx-auto px-6 py-10 lg:py-14">

        {/* Header */}
        <header className="flex flex-wrap items-end justify-between gap-6 mb-10">
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-full bg-[#5C7460] flex items-center justify-center">
                <Leaf size={15} className="text-[#F7F3EC]" strokeWidth={2.2} />
              </div>
              <span className="text-xs tracking-[0.22em] uppercase text-[#8A8273] font-semibold">Sanctuary Ledger</span>
            </div>
            <h1 className="serif text-4xl lg:text-[2.75rem] leading-[1.05] font-medium">
              Ubud retreat,<br />
              <span className="italic text-[#5C7460]">fourteen quiet days</span>
            </h1>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 bg-white border border-[#E5DDCD] rounded-full px-4 py-2.5 text-sm text-[#6E6757]">
              <CalendarDays size={15} />
              Oct 8 – Oct 22, 2024
              <ChevronDown size={14} className="text-[#B3A98F]" />
            </div>
            <button className="flex items-center gap-2 bg-[#2C2A24] text-[#F7F3EC] rounded-full px-5 py-2.5 text-sm font-semibold hover:bg-[#5C7460] transition-colors duration-300">
              <Plus size={15} strokeWidth={2.5} /> Log expense
            </button>
          </div>
        </header>

        {/* Top row */}
        <div className="grid lg:grid-cols-[1.1fr_1fr_1fr] gap-5 mb-5">

          {/* Budget card */}
          <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
            className="bg-[#2E372E] rounded-[28px] p-7 text-[#F1EEE4] relative overflow-hidden">
            <div className="absolute -right-16 -top-16 w-56 h-56 rounded-full border-[28px] border-[#3C463B] opacity-60" />
            <div className="absolute -right-6 -bottom-20 w-44 h-44 rounded-full bg-[#3C463B] opacity-50" />
            <div className="relative">
              <div className="flex items-center gap-2 text-[#A9B8A4] text-xs tracking-[0.18em] uppercase font-semibold mb-5">
                <Wallet size={14} /> Retreat budget
              </div>
              <div className="serif text-5xl font-medium mb-1">${remaining.toFixed(0)}<span className="text-xl text-[#A9B8A4]"> left</span></div>
              <div className="text-sm text-[#A9B8A4] mb-6">of ${BUDGET.toLocaleString()} · ${totalSpent.toFixed(0)} spent so far</div>
              <div className="h-2.5 rounded-full bg-[#414C40] overflow-hidden mb-3">
                <motion.div initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 1.2, ease: 'easeOut' }}
                  className="h-full rounded-full bg-gradient-to-r from-[#9DB48C] to-[#D9C58A]" />
              </div>
              <div className="flex justify-between text-xs text-[#8FA189]">
                <span>Day 7 of 14</span>
                <span className="font-semibold text-[#D9C58A]">{pct.toFixed(0)}% used</span>
              </div>
            </div>
          </motion.div>

          {/* Daily rhythm chart */}
          <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.08 }}
            className="bg-white border border-[#E9E1D2] rounded-[28px] p-7">
            <div className="flex items-start justify-between mb-1">
              <div>
                <div className="text-xs tracking-[0.18em] uppercase text-[#8A8273] font-semibold mb-2">Daily rhythm</div>
                <div className="serif text-3xl font-medium">$132<span className="text-base text-[#8A8273]"> avg / day</span></div>
              </div>
              <div className="flex items-center gap-1 text-xs font-semibold text-[#5C7460] bg-[#E8EFE6] rounded-full px-2.5 py-1">
                <TrendingDown size={13} /> 18% vs wk 1
              </div>
            </div>
            <div className="h-28 mt-3 -mx-2">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={TREND} margin={{ top: 6, right: 8, left: 8, bottom: 0 }}>
                  <defs>
                    <linearGradient id="sage" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#5C7460" stopOpacity={0.35} />
                      <stop offset="100%" stopColor="#5C7460" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="day" hide />
                  <YAxis hide />
                  <Tooltip
                    cursor={{ stroke: '#D6CDBE', strokeDasharray: '3 3' }}
                    contentStyle={{ background: '#2C2A24', border: 'none', borderRadius: 12, fontSize: 12, color: '#F7F3EC', padding: '8px 12px' }}
                    itemStyle={{ color: '#D9C58A' }}
                    labelStyle={{ color: '#A9A290', marginBottom: 2 }}
                    formatter={(v) => [`$${v}`, 'spent']}
                  />
                  <Area type="monotone" dataKey="amount" stroke="#5C7460" strokeWidth={2.5} fill="url(#sage)" dot={false} activeDot={{ r: 4, fill: '#5C7460', stroke: '#fff', strokeWidth: 2 }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-between text-[10px] text-[#B3A98F] font-semibold tracking-wide px-1">
              <span>OCT 8</span><span>OCT 11</span><span>OCT 14</span>
            </div>
          </motion.div>

          {/* Donut */}
          <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.16 }}
            className="bg-white border border-[#E9E1D2] rounded-[28px] p-7">
            <div className="text-xs tracking-[0.18em] uppercase text-[#8A8273] font-semibold mb-4">Where it flows</div>
            <div className="flex items-center gap-5">
              <div className="relative w-32 h-32 shrink-0">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={byCategory} dataKey="value" innerRadius={42} outerRadius={62} paddingAngle={3} startAngle={90} endAngle={-270} stroke="none">
                      {byCategory.map(c => <Cell key={c.key} fill={c.color} />)}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="serif text-lg font-medium">{byCategory.length}</span>
                  <span className="text-[9px] tracking-widest uppercase text-[#8A8273]">areas</span>
                </div>
              </div>
              <div className="space-y-2.5 flex-1">
                {byCategory.slice(0, 4).map(c => (
                  <div key={c.key} className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2 text-[#5A5446]">
                      <span className="w-2 h-2 rounded-full" style={{ background: c.color }} />
                      {c.label}
                    </div>
                    <span className="font-semibold tabular-nums">${c.value.toFixed(0)}</span>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Lower section */}
        <div className="grid lg:grid-cols-[1fr_320px] gap-5">

          {/* Transactions */}
          <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.22 }}
            className="bg-white border border-[#E9E1D2] rounded-[28px] p-7">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-5">
              <h2 className="serif text-2xl font-medium">Recent moments</h2>
              <div className="flex items-center gap-2 bg-[#F7F3EC] rounded-full px-4 py-2 text-sm text-[#8A8273] w-56">
                <Search size={14} />
                <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search expenses…"
                  className="bg-transparent outline-none w-full placeholder:text-[#B3A98F] text-[#2C2A24]" />
              </div>
            </div>

            {/* filter pills */}
            <div className="flex gap-2 overflow-x-auto pb-1 mb-5 pill-fade">
              <button onClick={() => setFilter('all')}
                className={`shrink-0 px-4 py-1.5 rounded-full text-sm font-semibold transition-all duration-300 ${filter === 'all' ? 'bg-[#2C2A24] text-[#F7F3EC]' : 'bg-[#F1EBDF] text-[#6E6757] hover:bg-[#E9E1D2]'}`}>
                All
              </button>
              {Object.entries(CATEGORIES).map(([key, c]) => (
                <button key={key} onClick={() => setFilter(key)}
                  className={`shrink-0 px-4 py-1.5 rounded-full text-sm font-semibold transition-all duration-300 ${filter === key ? 'text-white' : 'bg-[#F1EBDF] text-[#6E6757] hover:bg-[#E9E1D2]'}`}
                  style={filter === key ? { background: c.color } : {}}>
                  {c.label}
                </button>
              ))}
            </div>

            <div className="divide-y divide-[#F1EBDF]">
              <AnimatePresence initial={false}>
                {visible.map(t => {
                  const c = CATEGORIES[t.cat];
                  const Icon = c.icon;
                  return (
                    <motion.div key={t.id} layout initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                      className="flex items-center gap-4 py-3.5 group cursor-pointer">
                      <div className="w-11 h-11 rounded-2xl flex items-center justify-center shrink-0 transition-transform duration-300 group-hover:scale-105"
                        style={{ background: c.soft }}>
                        <Icon size={18} style={{ color: c.color }} strokeWidth={2} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold text-[15px] truncate group-hover:text-[#5C7460] transition-colors">{t.name}</div>
                        <div className="text-xs text-[#9A9181]">{t.note} · {c.label}</div>
                      </div>
                      <div className="text-right shrink-0">
                        <div className="font-semibold tabular-nums">−${t.amount.toFixed(2)}</div>
                        <div className="text-xs text-[#9A9181]">{t.day}, {t.date}</div>
                      </div>
                    </motion.div>
                  );
                })}
              </AnimatePresence>
              {visible.length === 0 && (
                <div className="py-10 text-center text-sm text-[#9A9181]">Nothing here — breathe easy.</div>
              )}
            </div>
          </motion.div>

          {/* Right column */}
          <div className="space-y-5">
            {/* Category budgets */}
            <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.28 }}
              className="bg-white border border-[#E9E1D2] rounded-[28px] p-7">
              <h3 className="serif text-xl font-medium mb-5">Intentions vs reality</h3>
              <div className="space-y-5">
                {[
                  { key: 'stay', budget: 800 },
                  { key: 'wellness', budget: 280 },
                  { key: 'food', budget: 250 },
                  { key: 'movement', budget: 160 },
                  { key: 'ceremony', budget: 120 },
                ].map(({ key, budget }) => {
                  const spent = byCategory.find(c => c.key === key)?.value || 0;
                  const c = CATEGORIES[key];
                  const p = Math.min((spent / budget) * 100, 100);
                  const over = spent > budget;
                  return (
                    <div key={key}>
                      <div className="flex justify-between text-sm mb-1.5">
                        <span className="font-semibold text-[#5A5446]">{c.label}</span>
                        <span className={`tabular-nums ${over ? 'text-[#C05B3E] font-semibold' : 'text-[#9A9181]'}`}>
                          ${spent.toFixed(0)} <span className="text-[#C5BCA8]">/ ${budget}</span>
                        </span>
                      </div>
                      <div className="h-1.5 rounded-full bg-[#F1EBDF] overflow-hidden">
                        <motion.div initial={{ width: 0 }} animate={{ width: `${p}%` }} transition={{ duration: 1, delay: 0.3 }}
                          className="h-full rounded-full" style={{ background: over ? '#C05B3E' : c.color }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </motion.div>

            {/* Insight card */}
            <motion.div initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.34 }}
              className="bg-[#EFE6D6] rounded-[28px] p-7 relative overflow-hidden">
              <div className="absolute -bottom-10 -right-10 w-36 h-36 rounded-full border border-[#D9C58A] opacity-60" />
              <div className="absolute -bottom-4 -right-4 w-20 h-20 rounded-full border border-[#D9C58A] opacity-60" />
              <div className="flex items-center gap-2 text-xs tracking-[0.18em] uppercase text-[#9C8650] font-semibold mb-3">
                <Sparkles size={14} /> Gentle insight
              </div>
              <p className="serif text-lg leading-snug text-[#4A4434] mb-4">
                You're spending <span className="italic">$23 less per day</span> than week one. At this pace, $312 stays in your pocket for the Nusa Penida extension.
              </p>
              <div className="flex gap-3">
                <div className="flex-1 bg-white/70 rounded-2xl p-3.5">
                  <div className="flex items-center gap-1 text-[#5C7460] text-xs font-semibold mb-1"><ArrowDownRight size={13} /> Spa & Healing</div>
                  <div className="font-semibold tabular-nums text-sm">$176 <span className="text-[#9A9181] font-normal">this wk</span></div>
                </div>
                <div className="flex-1 bg-white/70 rounded-2xl p-3.5">
                  <div className="flex items-center gap-1 text-[#C05B3E] text-xs font-semibold mb-1"><ArrowUpRight size={13} /> Nourishment</div>
                  <div className="font-semibold tabular-nums text-sm">$108 <span className="text-[#9A9181] font-normal">this wk</span></div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        <footer className="mt-10 text-center text-xs text-[#B3A98F] tracking-wide">
          Exchange rate locked at Rp 15,640 / USD · last synced 6 minutes ago
        </footer>
      </div>
    </div>
  );
}