"use client";

import { useEffect, useState, useCallback } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface Listing {
  id: number;
  title: string;
  price: number | null;       // CAD cents
  mileage: number | null;     // km
  year: number | null;
  make: string | null;
  model: string | null;
  location: string | null;
  source_url: string;
  deal_score: number | null;
}

function scoreColor(score: number | null): string {
  if (score === null) return "bg-gray-200 text-gray-500";
  if (score >= 85) return "bg-green-100 text-green-800";
  if (score >= 70) return "bg-yellow-100 text-yellow-800";
  return "bg-red-100 text-red-700";
}

function scoreLabel(score: number | null): string {
  if (score === null) return "—";
  if (score >= 85) return "Great Deal";
  if (score >= 70) return "Fair Deal";
  return "Overpriced";
}

function formatPrice(cents: number | null): string {
  if (cents === null) return "—";
  return "$" + (cents / 100).toLocaleString("en-CA", { maximumFractionDigits: 0 });
}

function formatMileage(km: number | null): string {
  if (km === null) return "—";
  return km.toLocaleString("en-CA") + " km";
}

function ListingCard({ listing }: { listing: Listing }) {
  return (
    <a
      href={listing.source_url}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-white rounded-2xl shadow-sm border border-gray-100 hover:shadow-md hover:border-gray-200 transition-all p-5 group"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-0.5">
            {listing.year} · {listing.make} · {listing.model}
          </p>
          <h3 className="text-sm font-semibold text-gray-900 leading-snug line-clamp-2 group-hover:text-blue-700 transition-colors">
            {listing.title}
          </h3>
        </div>
        {listing.deal_score !== null && (
          <div className={`shrink-0 flex flex-col items-center rounded-xl px-3 py-2 ${scoreColor(listing.deal_score)}`}>
            <span className="text-lg font-bold leading-none">{Math.round(listing.deal_score)}</span>
            <span className="text-[10px] font-medium mt-0.5">{scoreLabel(listing.deal_score)}</span>
          </div>
        )}
      </div>

      <div className="mt-4 flex flex-wrap gap-x-5 gap-y-1 text-sm text-gray-600">
        <span className="font-semibold text-gray-900 text-base">{formatPrice(listing.price)}</span>
        <span>{formatMileage(listing.mileage)}</span>
        {listing.location && <span className="text-gray-400">{listing.location}</span>}
      </div>
    </a>
  );
}

export default function Home() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [make, setMake] = useState("");
  const [model, setModel] = useState("");
  const [yearMin, setYearMin] = useState("");
  const [yearMax, setYearMax] = useState("");
  const [priceMax, setPriceMax] = useState("");
  const [mileageMax, setMileageMax] = useState("");

  const fetchListings = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (make)       params.set("make", make);
      if (model)      params.set("model", model);
      if (yearMin)    params.set("year_min", yearMin);
      if (yearMax)    params.set("year_max", yearMax);
      if (priceMax)   params.set("price_max", String(Math.round(parseFloat(priceMax) * 100)));
      if (mileageMax) params.set("mileage_max", mileageMax);

      const res = await fetch(`${API}/listings?${params}`);
      if (!res.ok) throw new Error(`API error ${res.status}`);
      setListings(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load listings");
    } finally {
      setLoading(false);
    }
  }, [make, model, yearMin, yearMax, priceMax, mileageMax]);

  useEffect(() => { fetchListings(); }, [fetchListings]);

  function handleReset() {
    setMake(""); setModel(""); setYearMin(""); setYearMax(""); setPriceMax(""); setMileageMax("");
  }

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold tracking-tight text-gray-900">Car Finder CA</h1>
            <p className="text-xs text-gray-400">Best used car deals in Canada, ranked by deal score</p>
          </div>
          <span className="text-xs text-gray-400 bg-gray-100 rounded-full px-3 py-1">
            {listings.length} listing{listings.length !== 1 ? "s" : ""}
          </span>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-6">
        {/* Filters */}
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 mb-6">
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Make</label>
              <input
                className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Toyota"
                value={make}
                onChange={e => setMake(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Model</label>
              <input
                className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Corolla"
                value={model}
                onChange={e => setModel(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Year from</label>
              <input
                type="number"
                className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="2015"
                value={yearMin}
                onChange={e => setYearMin(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Year to</label>
              <input
                type="number"
                className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="2024"
                value={yearMax}
                onChange={e => setYearMax(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Max price ($)</label>
              <input
                type="number"
                className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="30000"
                value={priceMax}
                onChange={e => setPriceMax(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">Max km</label>
              <input
                type="number"
                className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="100000"
                value={mileageMax}
                onChange={e => setMileageMax(e.target.value)}
              />
            </div>
          </div>
          <div className="mt-3 flex gap-2 justify-end">
            <button
              onClick={handleReset}
              className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Reset
            </button>
            <button
              onClick={fetchListings}
              className="text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white px-5 py-1.5 rounded-lg transition-colors"
            >
              Search
            </button>
          </div>
        </div>

        {/* Results */}
        {loading && (
          <div className="flex items-center justify-center py-24 text-gray-400">
            Loading listings…
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-2xl p-4 text-sm">
            {error} — is the backend running?
          </div>
        )}

        {!loading && !error && listings.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 text-gray-400">
            <p className="text-lg font-medium">No listings found</p>
            <p className="text-sm mt-1">Try adjusting your filters</p>
          </div>
        )}

        {!loading && !error && listings.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {listings.map(l => <ListingCard key={l.id} listing={l} />)}
          </div>
        )}
      </div>
    </main>
  );
}
