import { Calendar, MapPin, Users } from "lucide-react";
import { Button } from "@/components/ui/button";

type EventItem = {
  id: string;
  title: string;
  category: string;
  date: string;
  area: string;
  venue: string;
  price: string;
  attending: string;
  gradient: string;
  emoji: string;
};

const events: EventItem[] = [
  {
    id: "1",
    title: "Bad Bunny – Most Wanted Tour",
    category: "Concert",
    date: "Sat, Jun 14 · 9:00 PM",
    area: "Downtown Miami",
    venue: "Kaseya Center",
    price: "From $120",
    attending: "12.4k",
    gradient: "from-fuchsia-500 via-violet-500 to-indigo-500",
    emoji: "🎤",
  },
  {
    id: "2",
    title: "ReactConf US 2026",
    category: "Conference",
    date: "Thu, Jul 3 · 8:30 AM",
    area: "Brickell",
    venue: "Miami Convention Center",
    price: "From $95",
    attending: "1.8k",
    gradient: "from-cyan-400 via-sky-500 to-blue-600",
    emoji: "💻",
  },
  {
    id: "3",
    title: "Talk: The Art of Simplicity",
    category: "Talk",
    date: "Fri, May 22 · 7:00 PM",
    area: "Coconut Grove",
    venue: "Coconut Grove Playhouse",
    price: "From $35",
    attending: "640",
    gradient: "from-amber-400 via-orange-500 to-rose-500",
    emoji: "🎭",
  },
  {
    id: "4",
    title: "Ultra Music Festival",
    category: "Festival",
    date: "Fri, Mar 27 · 2:00 PM",
    area: "Downtown Miami",
    venue: "Bayfront Park",
    price: "From $320",
    attending: "45k",
    gradient: "from-emerald-400 via-teal-500 to-cyan-600",
    emoji: "🎶",
  },
  {
    id: "5",
    title: "Standup Night – Trevor Noah",
    category: "Talk",
    date: "Sat, May 31 · 8:30 PM",
    area: "South Beach",
    venue: "Fillmore Miami Beach",
    price: "From $60",
    attending: "1.2k",
    gradient: "from-pink-400 via-rose-500 to-red-500",
    emoji: "🎙️",
  },
];

export function EventList() {
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          <span className="font-semibold text-foreground">{events.length}</span> events found in
          Miami
        </p>
        <select className="text-sm bg-card border border-border rounded-full px-4 py-1.5 text-foreground focus:outline-none focus:ring-2 focus:ring-primary/30">
          <option>Most relevant</option>
          <option>Upcoming</option>
          <option>Price: low to high</option>
        </select>
      </div>

      {events.map((e) => (
        <article
          key={e.id}
          className="group flex flex-col sm:flex-row gap-5 rounded-3xl border border-border/60 bg-card p-4 shadow-sm hover:shadow-lg hover:border-primary/30 transition-all duration-300"
        >
          <div
            className={`relative flex-shrink-0 sm:w-48 h-40 sm:h-auto rounded-2xl bg-gradient-to-br ${e.gradient} flex items-center justify-center text-5xl overflow-hidden`}
          >
            <span className="drop-shadow-lg">{e.emoji}</span>
            <span className="absolute top-3 left-3 text-[10px] font-semibold uppercase tracking-wider bg-background/90 text-foreground px-2.5 py-1 rounded-full">
              {e.category}
            </span>
          </div>

          <div className="flex-1 flex flex-col justify-between gap-3">
            <div>
              <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition-colors">
                {e.title}
              </h3>
              <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-muted-foreground">
                <span className="inline-flex items-center gap-1.5">
                  <Calendar className="h-3.5 w-3.5" /> {e.date}
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <MapPin className="h-3.5 w-3.5" /> {e.venue}, {e.area}
                </span>
                <span className="inline-flex items-center gap-1.5">
                  <Users className="h-3.5 w-3.5" /> {e.attending} attending
                </span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-border/50">
              <span className="text-sm font-semibold text-foreground">{e.price} USD</span>
              <Button className="rounded-full bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity">
                Buy tickets
              </Button>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
