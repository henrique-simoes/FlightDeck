import { Search, MapPin, Calendar, Tag } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";

const categories = ["Concerts", "Conferences", "Talks", "Theater", "Sports", "Festivals"];
const areas = ["Downtown", "Wynwood", "South Beach", "Brickell", "Coconut Grove"];

export function EventFilters() {
  return (
    <div className="sticky top-24 rounded-3xl border border-border/60 bg-card p-6 shadow-sm">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-lg font-semibold text-foreground">Filters</h2>
        <Button variant="ghost" size="sm" className="text-xs text-muted-foreground rounded-full">
          Clear
        </Button>
      </div>

      <div className="space-y-6">
        <div className="space-y-2">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <Search className="h-3.5 w-3.5" /> Search
          </Label>
          <Input placeholder="Event name..." className="rounded-2xl" />
        </div>

        <div className="space-y-3">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <Tag className="h-3.5 w-3.5" /> Category
          </Label>
          <div className="space-y-2.5">
            {categories.map((c) => (
              <div key={c} className="flex items-center gap-2.5">
                <Checkbox id={c} defaultChecked={c === "Concerts"} className="rounded-md" />
                <label htmlFor={c} className="text-sm text-foreground cursor-pointer">
                  {c}
                </label>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <MapPin className="h-3.5 w-3.5" /> Area in Miami
          </Label>
          <div className="flex flex-wrap gap-2">
            {areas.map((c, i) => (
              <span
                key={c}
                className={`px-3 py-1 rounded-full text-xs font-medium cursor-pointer transition-colors ${
                  i === 0
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-secondary-foreground hover:bg-secondary/70"
                }`}
              >
                {c}
              </span>
            ))}
          </div>
        </div>

        <div className="space-y-3">
          <Label className="text-xs font-medium text-muted-foreground flex items-center gap-1.5">
            <Calendar className="h-3.5 w-3.5" /> Date
          </Label>
          <div className="grid grid-cols-2 gap-2">
            <Button variant="outline" size="sm" className="rounded-full text-xs">
              Today
            </Button>
            <Button variant="outline" size="sm" className="rounded-full text-xs">
              This week
            </Button>
            <Button variant="outline" size="sm" className="rounded-full text-xs">
              This month
            </Button>
            <Button variant="outline" size="sm" className="rounded-full text-xs">
              Custom
            </Button>
          </div>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <Label className="text-xs font-medium text-muted-foreground">Max price</Label>
            <span className="text-xs font-semibold text-primary">$250</span>
          </div>
          <Slider defaultValue={[250]} max={500} step={10} />
          <div className="flex justify-between text-[10px] text-muted-foreground">
            <span>$0</span>
            <span>$500</span>
          </div>
        </div>

        <Button className="w-full rounded-full bg-gradient-to-r from-primary to-accent hover:opacity-90 transition-opacity">
          Apply filters
        </Button>
      </div>
    </div>
  );
}
