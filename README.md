###################################
# This is a tools manage program.. #  
####################################
How to Use?
============================
1.source build.sh

2.cd master;
    use command :
    cst -h
3.new tools should be added in file master/tools and include xml file.
xml demo:
***************************************************************************************************
<?xml version="1.0" encoding="utf-8" ?>
<tool id="CheckBuild">
        <type>cmd</type>
        <command>python action.py</command>
        <description>¼ì²é°¢À­¶¡½¨¿â¶ËÎÊÌâ</description>
        <!-- kvÐÎÊ½µÄÊý¾Ý·¢²¼ÓëÒÀÀµÉùÃ÷ -->
        <depend_on>
            <key>Query</key>
            <key>SrcID</key>
        </depend_on>
        <dependency>
            <tool>test.sh</tool>
        </dependency>
        <publish>
            <key>BuildFailureDetails</key>
        </publish>
</tool>
***************************************************************************************************
root node must be used <tool> and include <dependency> node.













============================
problems if u meet:
1.bash: cst: command not found
    source ~/.bashrc
2.todo
