"use client";

import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";

import {
  ArrowUp,
  BatteryCharging,
  Check,
  Copy,
  ExternalLink,
  FileText,
  Headphones,
  Laptop,
  Menu,
  Plus,
  RotateCcw,
  Search,
  ShieldCheck,
  Sparkles,
  Wrench,
} from "lucide-react";

type Source = {
  document: string;
  page: number;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const bottomRef = useRef<HTMLDivElement | null>(null);

  const hasConversation = messages.length > 0;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function sendMessage(questionOverride?: string) {
    const question = (questionOverride ?? input).trim();

    if (!question || loading) return;

    const userMessage: Message = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer || "The API returned no answer.",
        sources: data.sources || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't connect to the AI service. Please check that the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    setMessages([]);
    setInput("");
  }

  async function copyAnswer(text: string, index: number) {
    await navigator.clipboard.writeText(text);

    setCopiedIndex(index);

    setTimeout(() => {
      setCopiedIndex(null);
    }, 1500);
  }

  async function regenerateAnswer(index: number) {
    if (loading) return;

    let previousUserQuestion = "";

    for (let i = index - 1; i >= 0; i--) {
      if (messages[i].role === "user") {
        previousUserQuestion = messages[i].content;
        break;
      }
    }

    if (!previousUserQuestion) return;

    setMessages((prev) =>
      prev.filter((_, messageIndex) => messageIndex !== index)
    );

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: previousUserQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: "assistant",
        content: data.answer || "The API returned no answer.",
        sources: data.sources || [],
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't regenerate the answer. Please check that the AI service is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen bg-[#0b0c0f] text-white">
      {/* SIDEBAR */}
      <aside className="hidden w-[270px] shrink-0 flex-col border-r border-white/10 bg-[#0c0e12] lg:flex">
        <div className="flex items-center gap-3 px-5 py-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white text-sm font-bold text-black">
            T
          </div>

          <div>
            <div className="font-semibold tracking-tight">ThinkAssist</div>
            <div className="text-xs text-zinc-500">AI Technical Support</div>
          </div>
        </div>

        <div className="px-4 pb-4">
          <button
            onClick={newChat}
            className="flex w-full items-center gap-3 rounded-xl bg-white px-4 py-3 text-sm font-medium text-black transition hover:bg-zinc-200"
          >
            <Plus size={17} />
            New chat
          </button>
        </div>

        <nav className="space-y-1 px-3">
          <a
            href="https://support.lenovo.com/us/en/solutions/ht516788"
            target="_blank"
            rel="noopener noreferrer"
            className="flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-white/5 hover:text-white"
          >
            <div className="flex items-center gap-3">
              <FileText size={17} />
              Knowledge base
            </div>

            <ExternalLink size={13} className="text-zinc-600" />
          </a>

          <a
            href="https://support.lenovo.com/us/en/selectproduct"
            target="_blank"
            rel="noopener noreferrer"
            className="flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-sm text-zinc-400 transition hover:bg-white/5 hover:text-white"
          >
            <div className="flex items-center gap-3">
              <Headphones size={17} />
              Lenovo Support
            </div>

            <ExternalLink size={13} className="text-zinc-600" />
          </a>
        </nav>

        <div className="mx-4 my-5 border-t border-white/10" />

        <div className="px-5">
          <p className="text-xs leading-5 text-zinc-600">
            Ask ThinkAssist about setup, hardware, battery, troubleshooting,
            recovery, warranty, and support for the ThinkPad P1 Gen 7.
          </p>
        </div>

        <div className="mt-auto p-4">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-4">
            <div className="flex items-center gap-3">
              <Laptop size={19} className="text-zinc-300" />

              <div>
                <p className="text-sm font-medium">ThinkPad P1 Gen 7</p>
                <p className="text-xs text-zinc-600">
                  Support knowledge available
                </p>
              </div>
            </div>

            <div className="mt-4 flex items-center gap-2 text-xs text-emerald-400">
              <div className="h-2 w-2 rounded-full bg-emerald-500" />
              Assistant online
            </div>
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <section className="relative flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="relative z-20 flex h-[68px] items-center justify-between border-b border-white/10 bg-[#0b0c0f]/80 px-5 backdrop-blur-xl lg:px-8">
          <div className="flex items-center gap-3">
            <button
              className="text-zinc-400 transition hover:text-white lg:hidden"
              aria-label="Open menu"
            >
              <Menu size={20} />
            </button>

            <div>
              <p className="text-sm font-medium">ThinkAssist</p>
              <p className="text-xs text-zinc-600">ThinkPad P1 Gen 7</p>
            </div>
          </div>

          <div className="hidden items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs text-zinc-400 sm:flex">
            <div className="h-2 w-2 rounded-full bg-emerald-500" />
            AI support online
          </div>
        </header>

        {!hasConversation ? (
          <div className="relative flex flex-1 flex-col overflow-hidden">
            <div
              className="absolute inset-0 bg-cover bg-center opacity-[0.18]"
              style={{
                backgroundImage: "url('/thinkpad-bg.jpg')",
              }}
            />

            <div className="absolute inset-0 bg-gradient-to-r from-[#0b0c0f] via-[#0b0c0f]/92 to-[#0b0c0f]/65" />
            <div className="absolute inset-0 bg-gradient-to-t from-[#0b0c0f] via-[#0b0c0f]/35 to-[#0b0c0f]/55" />

            <div className="relative z-10 mx-auto flex w-full max-w-5xl flex-1 flex-col justify-center px-6 py-12 lg:px-10">
              <div className="max-w-3xl">
                <div className="mb-5 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.22em] text-zinc-500">
                  <div className="h-px w-8 bg-red-500" />
                  Intelligent technical support
                </div>

                <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
                  Welcome to
                  <span className="block bg-gradient-to-r from-white via-zinc-200 to-zinc-500 bg-clip-text text-transparent">
                    ThinkAssist
                  </span>
                </h1>

                <p className="mt-5 max-w-2xl text-base leading-7 text-zinc-400 sm:text-lg">
                  Your AI assistant for the ThinkPad P1 Gen 7. Get clear
                  answers about setup, troubleshooting, battery, recovery,
                  hardware, warranty, and support.
                </p>
              </div>

              <div className="mt-10 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <CapabilityCard
                  icon={<Laptop size={20} />}
                  title="Setup & hardware"
                  subtitle="Ports, hardware and setup guidance"
                  prompt="What ports does this laptop have?"
                  onClick={sendMessage}
                />

                <CapabilityCard
                  icon={<Wrench size={20} />}
                  title="Troubleshooting"
                  subtitle="Find help for common technical problems"
                  prompt="How do I recover Windows?"
                  onClick={sendMessage}
                />

                <CapabilityCard
                  icon={<BatteryCharging size={20} />}
                  title="Battery & power"
                  subtitle="Battery replacement and safety"
                  prompt="Can I replace the built-in battery myself?"
                  onClick={sendMessage}
                />

                <CapabilityCard
                  icon={<ShieldCheck size={20} />}
                  title="Warranty & support"
                  subtitle="Warranty and support information"
                  prompt="Where can I find Lenovo technical support?"
                  onClick={sendMessage}
                />
              </div>

              <div className="mt-7 flex flex-wrap gap-3">
                <StatusPill
                  icon={<FileText size={13} />}
                  text="Technical documentation"
                />

                <StatusPill
                  icon={<Search size={13} />}
                  text="Intelligent search"
                />

                <StatusPill
                  icon={<Wrench size={13} />}
                  text="Support tools"
                />
              </div>

              <div className="mt-7 max-w-4xl">
                <Composer
                  input={input}
                  setInput={setInput}
                  loading={loading}
                  sendMessage={sendMessage}
                />

                <p className="mt-3 text-xs text-zinc-600">
                  Try saying hello or ask a question about your ThinkPad.
                </p>
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto">
              <div className="mx-auto max-w-3xl px-5 py-10">
                <div className="space-y-10">
                  {messages.map((message, index) => (
                    <div key={index}>
                      {message.role === "user" ? (
                        <div className="flex justify-end">
                          <div className="max-w-[82%] rounded-[22px] bg-zinc-800 px-5 py-3 text-[15px] leading-6">
                            {message.content}
                          </div>
                        </div>
                      ) : (
                        <AssistantMessage
                          message={message}
                          index={index}
                          copiedIndex={copiedIndex}
                          copyAnswer={copyAnswer}
                          regenerateAnswer={regenerateAnswer}
                          loading={loading}
                        />
                      )}
                    </div>
                  ))}

                  {loading && <ThinkingState />}

                  <div ref={bottomRef} />
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-t from-[#0b0c0f] via-[#0b0c0f] to-transparent px-4 pb-5 pt-7">
              <div className="mx-auto max-w-3xl">
                <Composer
                  input={input}
                  setInput={setInput}
                  loading={loading}
                  sendMessage={sendMessage}
                />

                <p className="mt-2 text-center text-[11px] text-zinc-700">
                  ThinkAssist may make mistakes. Review important information
                  before making hardware changes.
                </p>
              </div>
            </div>
          </>
        )}
      </section>
    </main>
  );
}

function CapabilityCard({
  icon,
  title,
  subtitle,
  prompt,
  onClick,
}: {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  prompt: string;
  onClick: (prompt: string) => void;
}) {
  return (
    <button
      onClick={() => onClick(prompt)}
      className="group rounded-2xl border border-white/10 bg-white/[0.055] p-5 text-left backdrop-blur-md transition hover:-translate-y-0.5 hover:border-white/20 hover:bg-white/[0.08]"
    >
      <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-black/20 text-zinc-300 transition group-hover:text-white">
        {icon}
      </div>

      <p className="text-sm font-medium">{title}</p>

      <p className="mt-1 text-xs leading-5 text-zinc-500">{subtitle}</p>
    </button>
  );
}

function StatusPill({
  icon,
  text,
}: {
  icon: React.ReactNode;
  text: string;
}) {
  return (
    <div className="flex items-center gap-2 rounded-full border border-white/10 bg-black/20 px-3 py-1.5 text-xs text-zinc-500 backdrop-blur">
      {icon}
      {text}
    </div>
  );
}

function Composer({
  input,
  setInput,
  loading,
  sendMessage,
}: {
  input: string;
  setInput: (value: string) => void;
  loading: boolean;
  sendMessage: (questionOverride?: string) => void;
}) {
  return (
    <div className="flex items-end gap-3 rounded-[24px] border border-white/15 bg-[#181a1f]/90 p-3 shadow-2xl backdrop-blur-xl transition focus-within:border-white/25">
      <textarea
        value={input}
        onChange={(event) => {
          setInput(event.target.value);

          event.target.style.height = "auto";
          event.target.style.height =
            Math.min(event.target.scrollHeight, 160) + "px";
        }}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
          }
        }}
        rows={1}
        placeholder="Ask anything about your ThinkPad..."
        className="max-h-40 min-h-[46px] flex-1 resize-none overflow-y-auto bg-transparent px-3 py-3 text-[15px] text-zinc-100 outline-none placeholder:text-zinc-600"
      />

      <button
        onClick={() => sendMessage()}
        disabled={loading || !input.trim()}
        className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-red-600 text-white transition hover:bg-red-500 disabled:cursor-not-allowed disabled:bg-zinc-700 disabled:text-zinc-500"
        aria-label="Send message"
      >
        <ArrowUp size={19} />
      </button>
    </div>
  );
}

function AssistantMessage({
  message,
  index,
  copiedIndex,
  copyAnswer,
  regenerateAnswer,
  loading,
}: {
  message: Message;
  index: number;
  copiedIndex: number | null;
  copyAnswer: (text: string, index: number) => void;
  regenerateAnswer: (index: number) => void;
  loading: boolean;
}) {
  return (
    <div>
      <div className="mb-4 flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-white text-black">
          <Sparkles size={15} />
        </div>

        <span className="text-sm font-medium">ThinkAssist</span>
      </div>

      <div className="pl-11">
        <div className="text-[15px] leading-7 text-zinc-200">
          <ReactMarkdown
            components={{
              p: ({ children }) => (
                <p className="mb-3 last:mb-0">{children}</p>
              ),

              ul: ({ children }) => (
                <ul className="mb-4 list-disc space-y-1 pl-5">
                  {children}
                </ul>
              ),

              ol: ({ children }) => (
                <ol className="mb-4 list-decimal space-y-1 pl-5">
                  {children}
                </ol>
              ),

              strong: ({ children }) => (
                <strong className="font-semibold text-white">
                  {children}
                </strong>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {message.sources && message.sources.length > 0 && (
          <div className="mt-6">
            <p className="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-600">
              Sources
            </p>

            <div className="flex flex-wrap gap-2">
              {message.sources.map((source, sourceIndex) => (
                <SourceCard
                  key={`${source.document}-${source.page}-${sourceIndex}`}
                  source={source}
                />
              ))}
            </div>
          </div>
        )}

        <div className="mt-4 flex items-center gap-1">
          <button
            onClick={() => copyAnswer(message.content, index)}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-600 transition hover:bg-white/5 hover:text-zinc-300"
            aria-label="Copy answer"
            title="Copy answer"
          >
            {copiedIndex === index ? (
              <Check size={15} />
            ) : (
              <Copy size={15} />
            )}
          </button>

          <button
            onClick={() => regenerateAnswer(index)}
            disabled={loading}
            className="flex h-8 w-8 items-center justify-center rounded-lg text-zinc-600 transition hover:bg-white/5 hover:text-zinc-300 disabled:cursor-not-allowed disabled:opacity-40"
            aria-label="Regenerate answer"
            title="Regenerate answer"
          >
            <RotateCcw size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}

function SourceCard({ source }: { source: Source }) {
  const displayName = getFriendlyDocumentName(source.document);

  return (
    <div className="flex max-w-full items-center gap-2 rounded-xl border border-white/10 bg-white/[0.035] px-3 py-2.5 transition hover:border-white/20 hover:bg-white/[0.055]">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white/[0.05] text-zinc-400">
        <FileText size={14} />
      </div>

      <div className="min-w-0">
        <p className="truncate text-xs font-medium text-zinc-300">
          {displayName}
        </p>

        <p className="text-[11px] text-zinc-600">Page {source.page}</p>
      </div>
    </div>
  );
}

function getFriendlyDocumentName(document: string) {
  const normalized = document.toLowerCase();

  if (normalized.includes("warranty")) {
    return "Safety & Warranty Guide";
  }

  if (normalized.includes("setup")) {
    return "Setup Guide";
  }

  if (normalized.includes("userguide")) {
    return "User Guide";
  }

  return document
    .replace(".pdf", "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function ThinkingState() {
  return (
    <div>
      <div className="mb-4 flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-white text-black">
          <Sparkles size={15} />
        </div>

        <span className="text-sm font-medium">ThinkAssist</span>
      </div>

      <div className="flex items-center gap-1.5 pl-11">
        <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-500 [animation-delay:-0.3s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-500 [animation-delay:-0.15s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-zinc-500" />

        <span className="ml-2 text-xs text-zinc-600">
          Searching support documentation...
        </span>
      </div>
    </div>
  );
}