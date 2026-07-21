type Props = {
  title: string;
  value: string | number;
};

export default function StatCard({ title, value }: Props) {
  return (
    <div className="rounded-xl border p-5">
      <p className="text-sm text-gray-500">{title}</p>

      <h1 className="text-3xl font-bold mt-2">
        {value}
      </h1>
    </div>
  );
}