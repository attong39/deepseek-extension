import { HealthBadge } from "@/components/dashboard/HealthBadge";
import { StatsCard } from "@/components/stats/StatsCard";
import OneClickDropzone from "@/features/training/oneClick/Dropzone";
import { BUILD_INFO } from "@/services/buildInfo";
import Click from "Click";
import Dashboard from "./Dashboard";
import Dropzone from "../training/oneClick/Dropzone";
import Jobs from "Jobs";
import Learning from "Learning";
import One from "One";

export default function Dashboard() {
  return (
    <div className="p-4 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-semibold">Bảng điều khiển</h1>
        <HealthBadge />
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatsCard title="Jobs hôm nay" value={3} hint="đã chạy" />
        <StatsCard title="Thành công" value="100%" hint="7 ngày" />
        <StatsCard title="Tệp chờ xử lý" value={0} />
        <StatsCard title="Phiên bản" value={BUILD_INFO.version} />
      </div>
      
      <section className="mt-4">
        <h2 className="text-lg mb-2">One-Click Learning</h2>
        <OneClickDropzone />
      </section>
    </div>
  );
}
