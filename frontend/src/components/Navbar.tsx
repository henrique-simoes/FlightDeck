import { Ticket, Bell, Search } from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-border/60 bg-background/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8 h-16">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-accent text-primary-foreground shadow-md">
            <Ticket className="h-5 w-5" />
          </div>
          <span className="text-lg font-bold tracking-tight bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Eventinkerer
          </span>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-muted-foreground">
          <a className="hover:text-foreground transition-colors">Explore</a>
          <a className="hover:text-foreground transition-colors">Categories</a>
          <a className="hover:text-foreground transition-colors">My tickets</a>
        </nav>

        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" className="rounded-full">
            <Search className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="rounded-full relative">
            <Bell className="h-4 w-4" />
            <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-accent" />
          </Button>
          <div className="hidden sm:flex flex-col items-end leading-tight">
            <span className="text-sm font-semibold text-foreground">Sofia Martinez</span>
            <span className="text-xs text-muted-foreground">Premium</span>
          </div>
          <Avatar className="h-9 w-9 ring-2 ring-primary/30">
            <AvatarImage src="https://i.pravatar.cc/100?img=47" alt="Sofia" />
            <AvatarFallback>SM</AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  );
}
