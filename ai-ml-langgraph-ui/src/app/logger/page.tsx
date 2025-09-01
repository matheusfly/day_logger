"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@radix-ui/react-label";

export default function LoggerPage() {
  const [morning, setMorning] = useState({startTime: "09:00", endTime: "12:00", content: ""});
  const [midday, setMidday] = useState({startTime: "12:00", endTime: "17:00", content: ""});
  const [evening, setEvening] = useState({startTime: "17:00", endTime: "21:00", content: ""});

  const handleSaveJournal = () => {
    const journalData = {
      morning: { start_time: morning.startTime, end_time: morning.endTime, content: morning.content },
      midday: { start_time: midday.startTime, end_time: midday.endTime, content: midday.content },
      evening: { start_time: evening.startTime, end_time: evening.endTime, content: evening.content },
    };

    if (window.electron) {
      window.electron.ipcRenderer.sendMessage('save-journal', journalData);
    }
  };

  useEffect(() => {
    if (window.electron) {
        const removeListener = window.electron.ipcRenderer.on('save-journal-reply', (response) => {
            console.log('Received from main:', response);
            // here I can show a toast notification
        });
        return () => {
            removeListener();
        };
    }
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold">Day Logger</h1>
        </div>
      </header>
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="journal" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="journal">Journal</TabsTrigger>
            <TabsTrigger value="dreams">Dreams</TabsTrigger>
            <TabsTrigger value="objectives">Objectives</TabsTrigger>
            <TabsTrigger value="goals">Goals</TabsTrigger>
            <TabsTrigger value="tasks">Tasks</TabsTrigger>
          </TabsList>
          <TabsContent value="journal">
            <Card>
              <CardHeader>
                <CardTitle>Daily Journal</CardTitle>
                <CardDescription>
                  Record your daily tasks and activities.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Morning Tasks */}
                <div className="space-y-2">
                  <h3 className="text-lg font-semibold">Morning Tasks</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="morning-start-time">Start Time</Label>
                      <Input id="morning-start-time" type="time" value={morning.startTime} onChange={(e) => setMorning({...morning, startTime: e.target.value})} />
                    </div>
                    <div>
                      <Label htmlFor="morning-end-time">End Time</Label>
                      <Input id="morning-end-time" type="time" value={morning.endTime} onChange={(e) => setMorning({...morning, endTime: e.target.value})} />
                    </div>
                  </div>
                  <Textarea
                    placeholder="Enter your morning tasks here..."
                    value={morning.content}
                    onChange={(e) => setMorning({...morning, content: e.target.value})}
                  />
                </div>
                {/* Mid-day Tasks */}
                <div className="space-y-2">
                  <h3 className="text-lg font-semibold">Mid-day Tasks</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="midday-start-time">Start Time</Label>
                      <Input id="midday-start-time" type="time" value={midday.startTime} onChange={(e) => setMidday({...midday, startTime: e.target.value})} />
                    </div>
                    <div>
                      <Label htmlFor="midday-end-time">End Time</Label>
                      <Input id="midday-end-time" type="time" value={midday.endTime} onChange={(e) => setMidday({...midday, endTime: e.target.value})} />
                    </div>
                  </div>
                  <Textarea
                    placeholder="Enter your mid-day tasks here..."
                    value={midday.content}
                    onChange={(e) => setMidday({...midday, content: e.target.value})}
                  />
                </div>
                {/* Evening Tasks */}
                <div className="space-y-2">
                  <h3 className="text-lg font-semibold">Evening Tasks</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="evening-start-time">Start Time</Label>
                      <Input id="evening-start-time" type="time" value={evening.startTime} onChange={(e) => setEvening({...evening, startTime: e.target.value})} />
                    </div>
                    <div>
                      <Label htmlFor="evening-end-time">End Time</Label>
                      <Input id="evening-end-time" type="time" value={evening.endTime} onChange={(e) => setEvening({...evening, endTime: e.target.value})} />
                    </div>
                  </div>
                  <Textarea
                    placeholder="Enter your evening tasks here..."
                    value={evening.content}
                    onChange={(e) => setEvening({...evening, content: e.target.value})}
                  />
                </div>
                <Button onClick={handleSaveJournal}>Save Journal</Button>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="dreams">
            <p>Dreams management will be here.</p>
          </TabsContent>
          <TabsContent value="objectives">
            <p>Objectives management will be here.</p>
          </TabsContent>
          <TabsContent value="goals">
            <p>Goals management will be here.</p>
          </TabsContent>
          <TabsContent value="tasks">
            <p>Tasks management will be here.</p>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
