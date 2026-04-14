import asyncio

from fastmcp import Client
from app.mcp.server import mcp

from app.mcp import tools  # noqa: F401
from app.mcp import resources  # noqa: F401
from app.mcp import prompts  # noqa: F401


async def main():
    client = Client(mcp)

    async with client:
        print("\n--- TOOLS ---")
        tools_list = await client.list_tools()
        for tool in tools_list:
            print(tool)

        print("\n--- RESOURCES ---")
        resources_list = await client.list_resources()
        for resource in resources_list:
            print(resource)

        print("\n--- PROMPTS ---")
        prompts_list = await client.list_prompts()
        for prompt in prompts_list:
            print(prompt)

        print("\n--- CALL TOOL: list_students_tool ---")
        result = await client.call_tool("list_students_tool", {})
        print(result)

        print("\n--- CALL TOOL: list_courses_tool ---")
        result = await client.call_tool("list_courses_tool", {})
        print(result)

        print("\n--- READ RESOURCE: school://schema ---")
        resource = await client.read_resource("school://schema")
        print(resource)

        print("\n--- READ RESOURCE: school://report/courses ---")
        resource = await client.read_resource("school://report/courses")
        print(resource)

        print("\n--- GET PROMPT: academic_assistant_prompt ---")
        prompt = await client.get_prompt("academic_assistant_prompt", {})
        print(prompt)

        print("\n--- TEST 1: duplicate student email ---")
        result = await client.call_tool(
            "create_student_tool",
            {
                "name": "Ana Duplicate",
                "email": "ana@example.com"
            }
        )
        print(result)

        print("\n--- TEST 2: full course ---")
        result = await client.call_tool(
            "create_course_tool",
            {
                "name": "Operating Systems",
                "description": "OS basics",
                "capacity": 1
            }
        )
        print("Created course:", result)

        result = await client.call_tool(
            "create_student_tool",
            {
                "name": "Student One",
                "email": "student1@example.com"
            }
        )
        print("Created student 1:", result)

        result = await client.call_tool(
            "create_student_tool",
            {
                "name": "Student Two",
                "email": "student2@example.com"
            }
        )
        print("Created student 2:", result)

        result = await client.call_tool(
            "enroll_student_by_email_tool",
            {
                "email": "student1@example.com",
                "course_id": 2
            }
        )
        print("First enrollment:", result)

        result = await client.call_tool(
            "enroll_student_by_email_tool",
            {
                "email": "student2@example.com",
                "course_id": 2
            }
        )
        print("Second enrollment attempt:", result)

        print("\n--- TEST 3: student not found ---")
        result = await client.call_tool(
            "get_student_tool",
            {
                "student_id": 999
            }
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(main())