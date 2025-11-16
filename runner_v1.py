#!/usr/bin/env python3
"""
Pipeline Runner v1: Single job executor
Executes one job in a Docker container and streams logs
"""

import yaml
import subprocess
import sys
from pathlib import Path


class Job:
    """Represents a single pipeline job."""

    def __init__(self, name, config):
        self.name = name
        self.image = config.get('image', 'python:3.11')
        self.script = config.get('script', [])
        self.stage = config.get('stage', 'test')

    def __repr__(self):
        return f"Job({self.name}, stage={self.stage})"


class JobExecutor:
    """Executes a job in a Docker container."""

    def __init__(self, workspace):
        self.workspace = Path(workspace).resolve()

    def run(self, job):
        """Execute a job and stream output."""
        print(f"\n{'='*60}")
        print(f"[{job.name}] Starting job...")
        print(f"[{job.name}] Image: {job.image}")
        print(f"[{job.name}] Stage: {job.stage}")
        print(f"{'='*60}\n")

        # Combine all script commands into one shell command
        script = ' && '.join(job.script)

        # Build docker run command
        cmd = [
            'docker', 'run',
            '--rm',  # Remove container after execution
            '-v', f'{self.workspace}:/workspace',  # Mount workspace
            '-w', '/workspace',  # Set working directory
            job.image,
            'sh', '-c', script
        ]

        try:
            # Run and stream output in real-time
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Stream output line by line
            for line in process.stdout:
                print(f"[{job.name}] {line}", end='')

            process.wait()

            if process.returncode == 0:
                print(f"\n[{job.name}] ✓ Job completed successfully\n")
                return True
            else:
                print(f"\n[{job.name}] ✗ Job failed with exit code {process.returncode}\n")
                return False

        except Exception as e:
            print(f"\n[{job.name}] ✗ Error: {e}\n")
            return False


class Pipeline:
    """Represents a pipeline with jobs."""

    def __init__(self, config_file):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.jobs = self._parse_jobs()

    def _load_config(self):
        """Load and parse YAML configuration."""
        with open(self.config_file) as f:
            return yaml.safe_load(f)

    def _parse_jobs(self):
        """Parse jobs from configuration."""
        jobs = []
        for job_name, job_config in self.config.items():
            if job_name != 'stages' and isinstance(job_config, dict):
                jobs.append(Job(job_name, job_config))
        return jobs

    def run(self, workspace='.'):
        """Execute all jobs sequentially."""
        print(f"\nStarting pipeline from {self.config_file}")
        print(f"Found {len(self.jobs)} job(s)\n")

        executor = JobExecutor(workspace)

        for job in self.jobs:
            success = executor.run(job)
            if not success:
                print("Pipeline failed!")
                return False

        print("✓ Pipeline completed successfully!")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner_v1.py <pipeline.yml>")
        sys.exit(1)

    pipeline = Pipeline(sys.argv[1])
    success = pipeline.run()
    sys.exit(0 if success else 1)