### Диаграмма последовательности выполнения проекта
```mermaid
sequenceDiagram
    participant Browser
    participant Server
    participant Container_Manager
    participant Container
    
    Browser-)Server: run project
    Server-)Container_Manager: init volume
    
    loop project lifetime
        Container_Manager-)Container: create container (one command)
        
        loop one command lifetime
            Container-)Server: stdout, stderr
            Server-)Browser: stdout, stderr
            Browser-)Server: stdin
            Server-)Container: stdin
        end
        Container-)Server: exit code (command end)
        Server-)Browser:  exit code
    end
```