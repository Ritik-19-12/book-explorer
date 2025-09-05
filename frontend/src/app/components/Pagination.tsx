export default function Pagination({
  total,
  page,
  setPage,
}: {
  total: number;
  page: number;
  setPage: (p: number) => void;
}) {
  const perPage = 20;
  const totalPages = Math.ceil(total / perPage);

  return (
    <div className="mt-6 flex justify-between items-center">
      <div>Total Books: {total}</div>
      <div>
        <button
          className="px-3 py-1 border mr-2"
          onClick={() => setPage(Math.max(1, page - 1))}
          disabled={page <= 1}
        >
          Prev
        </button>
        <span className="px-2">{page}</span>
        <button
          className="px-3 py-1 border"
          onClick={() => setPage(Math.min(totalPages, page + 1))}
          disabled={page >= totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
}
