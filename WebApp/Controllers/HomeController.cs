using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Diagnostics;
using WebApp.Models;
using WebApp.Data;
using WebApp.Controllers;

namespace WebApp.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly WebAppContext _context;

        public HomeController(ILogger<HomeController> logger, WebAppContext context)
        {
            _logger = logger;
            _context = context;
        }

        public IActionResult Login()
        {
            return View();
        }

        // POST: Users/Create
        // To protect from overposting attacks, enable the specific properties you want to bind to.
        // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
        /*[HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Id,UserName")] User user)
        {
            if (ModelState.IsValid)
            {
                var user = await _context.User
                    .FirstOrDefaultAsync(m => m.StudentId == user.StudentId);
                if (user == null)
                {
                    _context.Add(user____);
                    await _context.SaveChangesAsync();
                }
                return RedirectToAction(nameof(Index), nameof(QuestionController)); // I hope this works. 
            }
            return View(user);
        }

        public IActionResult Logout()
        {
            return View();
        }
        */
        //[Authorize]
        //public IActionResult Question()
        //{
        //    return View();
        //}

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}