interface StatsCardProps {
  label: string;
  value: number;
  bgColor?: string;
  textColor?: string;
}

export default function StatsCard({
  label,
  value,
  bgColor = 'bg-white',
  textColor = 'text-gray-900'
}: StatsCardProps) {
  return (
    <div className={`${bgColor} rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow`}>
      <div className="flex flex-col">
        <span className={`text-3xl font-bold ${textColor}`}>{value}</span>
        <span className="text-sm text-gray-500 mt-1">{label}</span>
      </div>
    </div>
  );
}
