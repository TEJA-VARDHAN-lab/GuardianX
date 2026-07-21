export default function LiveCamera() {
  return (
    <div className="rounded-2xl border bg-background shadow-sm overflow-hidden">

      <div className="flex items-center justify-between px-5 py-3 border-b">

        <div>
          <h2 className="font-semibold text-lg">
            Live Camera
          </h2>

          <p className="text-xs text-muted-foreground">
            AI Detection Stream
          </p>
        </div>


        <span className="flex items-center gap-2 text-xs font-semibold text-green-600">
          <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
          LIVE
        </span>

      </div>


      <div className="aspect-video bg-black">

        <img
          src="http://127.0.0.1:8000/api/v1/cameras/stream"
          alt="GuardianX Camera"
          className="w-full h-full object-cover"
        />

      </div>

    </div>
  );
}