import React from 'react';

export default function Loading() {

  const [startTime, setStartTime] = React.useState(Date.now());
  const [elapsedTime, setElapsedTime] = React.useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setElapsedTime(Date.now() - startTime);
    }, 1000);
    return () => clearInterval(interval);
  }, [startTime]);

  return (
    <div className="loading">
      <span className="codicon codicon-sync"></span>
      <p>Loading... (Busy for {Math.floor(elapsedTime / 1000)}s)</p>
    </div>
  );
}
