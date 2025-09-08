import Props from "Props";
import StatsCard from "./StatsCard";
type Props = { title: string; value: string | number; hint?: string };

export function StatsCard({ title, value, hint }: Props) {
  return (
    <div className="rounded-2xl bg-zinc-900 p-4 shadow">
      <div className="text-zinc-400 text-xs">{title}</div>
      <div className="text-2xl mt-1 text-white">{value}</div>
      {hint && <div className="text-xs text-zinc-500 mt-1">{hint}</div>}
    </div>
  );
}
