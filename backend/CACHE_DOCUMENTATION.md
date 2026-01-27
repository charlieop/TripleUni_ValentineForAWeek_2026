# Cache Documentation

This document provides a comprehensive overview of all cache keys used in the application, their purposes, timeouts, and invalidation strategies.

## Cache Backend

The application uses Django's **LocMemCache** (local memory cache) as configured in `server/settings.py`. This is an in-memory cache that stores data in the process memory.

## Cache Key Patterns

All cache keys follow a hierarchical naming convention using colons (`:`) as separators. This allows for organized cache management and easy navigation in the admin interface.

---

## Cache Keys Reference

### 1. Application Configuration

#### `app_config`
- **Type**: `Config` model instance
- **Purpose**: Caches the singleton application configuration object
- **Timeout**: `None` (no expiration, manually invalidated)
- **Set in**: `main/models/config.py::Config.load()`
- **Invalidated in**: 
  - `main/models/config.py::Config.save()` - when config is updated
- **Usage**: 
  - Loaded via `Config.load()` class method
  - Used throughout the application to access system configuration (maintenance mode, timezone, activity dates, etc.)

---

### 2. Token-Based Authentication Cache

These cache keys store authentication-related data keyed by user token.

#### `token:{token}:openid`
- **Type**: `str` (OpenID string)
- **Purpose**: Maps a user token to their WeChat OpenID
- **Timeout**: `3600` seconds (1 hour)
- **Set in**: `main/mixin.py::UtilMixin.get_openid_by_token()`
- **Invalidated in**:
  - `main/models/token.py::Token.save()` - when token is saved
  - `main/models/token.py::Token.delete()` - when token is deleted
  - `main/models/wechat_info.py::WeChatInfo.save()` - when WeChat info is updated
  - `main/models/wechat_info.py::WeChatInfo.delete()` - when WeChat info is deleted

#### `token:{token}:wechat_info`
- **Type**: `WeChatInfo` model instance
- **Purpose**: Caches the WeChat information object for a given token
- **Timeout**: `3600` seconds (1 hour)
- **Set in**: `main/mixin.py::UtilMixin.get_wechat_info_by_token()`
- **Invalidated in**:
  - `main/models/token.py::Token.save()` - when token is saved
  - `main/models/token.py::Token.delete()` - when token is deleted
  - `main/models/wechat_info.py::WeChatInfo.save()` - when WeChat info is updated
  - `main/models/wechat_info.py::WeChatInfo.delete()` - when WeChat info is deleted

#### `token:{token}:applicant`
- **Type**: `Applicant` model instance
- **Purpose**: Caches the applicant object for a given token
- **Timeout**: `3600` seconds (1 hour)
- **Set in**: `main/mixin.py::UtilMixin.get_applicant_by_token()`
- **Invalidated in**:
  - `main/models/token.py::Token.save()` - when token is saved
  - `main/models/token.py::Token.delete()` - when token is deleted
  - `main/models/wechat_info.py::WeChatInfo.save()` - when WeChat info is updated
  - `main/models/wechat_info.py::WeChatInfo.delete()` - when WeChat info is deleted
  - `main/models/applicant.py::Applicant.save()` - when applicant is updated
  - `main/models/applicant.py::Applicant.delete()` - when applicant is deleted

---

### 3. Applicant Cache

#### `applicant:openid:{openid}`
- **Type**: `Applicant` model instance
- **Purpose**: Maps a WeChat OpenID to the corresponding applicant object
- **Timeout**: `3600` seconds (1 hour)
- **Set in**: `main/mixin.py::UtilMixin.get_applicant_by_openid()`
- **Invalidated in**:
  - `main/models/applicant.py::Applicant.save()` - when applicant is updated
  - `main/models/applicant.py::Applicant.delete()` - when applicant is deleted
  - `main/models/wechat_info.py::WeChatInfo.save()` - when WeChat info is updated (if openid changes)
  - `main/models/wechat_info.py::WeChatInfo.delete()` - when WeChat info is deleted

---

### 4. Match Cache

#### `match:applicant:{applicant_id}`
- **Type**: `tuple[Match, int]` - (match object, position: 1 or 2)
- **Purpose**: Caches the match and position (applicant1 or applicant2) for a given applicant
- **Timeout**: `3600` seconds (1 hour)
- **Set in**: `main/mixin.py::UtilMixin.get_match_by_applicant()`
- **Invalidated in**:
  - `main/models/match.py::Match.save()` - when match is updated (if applicants change)
  - `main/models/match.py::Match.delete()` - when match is deleted
  - `main/models/applicant.py::Applicant.save()` - when applicant is updated
  - `main/models/applicant.py::Applicant.delete()` - when applicant is deleted
  - `main/models/task.py::Task.save()` - when task is updated (to reflect match changes)
  - `main/models/task.py::Task.delete()` - when task is deleted

---

### 5. Task Cache

#### `task:match:{match_id}:day:{day}`
- **Type**: `Task` model instance
- **Purpose**: Caches a task object for a specific match and day (1-7)
- **Timeout**: `3600` seconds (1 hour)
- **Set in**: `main/mixin.py::UtilMixin.get_task_by_match_and_day()`
- **Invalidated in**:
  - `main/models/task.py::Task.save()` - when task is updated (for current and old match/day if changed)
  - `main/models/task.py::Task.delete()` - when task is deleted

---

### 6. Ranking Cache

#### `match:ranking:all`
- **Type**: `dict[int, int]` - Dictionary mapping match_id to rank
- **Purpose**: Caches the complete ranking of all matches based on total scores
- **Timeout**: `900` seconds (15 minutes)
- **Set in**: `main/mixin.py::UtilMixin.get_rank()`
- **Invalidated in**:
  - `main/models/match.py::Match.delete()` - when a match is deleted
  - `main/models/task.py::Task.delete()` - when a task is deleted (affects scores)
- **Note**: 
  - This cache is NOT invalidated on task updates to allow the ranking to persist for the full 15 minutes
  - The ranking will be recalculated automatically after cache expiration
  - Handles ties properly: matches with the same score get the same rank

---

## Cache Invalidation Strategy

### Automatic Invalidation

The application uses a **write-through cache invalidation** strategy:

1. **On Model Save**: When a model is saved, all related cache keys are automatically deleted
2. **On Model Delete**: When a model is deleted, all related cache keys are automatically deleted
3. **Cascade Invalidation**: Related cache keys are invalidated to maintain data consistency

### Manual Invalidation

Cache can be manually cleared through:
- **Admin Interface**: Cache Management page (`/admin/cache-management/`)
  - Clear all cache
  - Delete individual cache keys
  - View cache hierarchy

### Cache Warming

The application uses **lazy loading** for cache:
- Cache entries are created on first access (cache miss)
- No pre-warming strategy is implemented
- Cache is populated as users interact with the system

---

## Cache Performance Considerations

### Timeout Strategy

1. **Short-lived caches (15 minutes)**:
   - `match:ranking:all` - Frequently changing data that benefits from short cache duration

2. **Medium-lived caches (1 hour)**:
   - All token-based caches
   - Applicant caches
   - Match caches
   - Task caches
   - These represent user session data that changes infrequently

3. **Permanent caches (no timeout)**:
   - `app_config` - Manually invalidated only when config is updated

### Memory Considerations

Since LocMemCache stores data in process memory:
- Cache size is limited by available RAM
- Cache is cleared when the Django process restarts
- No persistence across server restarts
- Suitable for single-server deployments

For multi-server deployments, consider switching to:
- **Redis** - Distributed cache with persistence
- **Memcached** - Distributed memory cache

---

## Cache Key Naming Convention

All cache keys follow this pattern:
```
{category}:{identifier}:{sub_identifier}
```

Examples:
- `token:{token}:openid` - Token category, token identifier, openid sub-identifier
- `match:applicant:{id}` - Match category, applicant identifier
- `task:match:{id}:day:{day}` - Task category, match identifier, day sub-identifier

This hierarchical structure:
- Makes cache keys easy to understand
- Enables efficient cache management in admin interface
- Allows for pattern-based cache invalidation (if needed)

---

## Monitoring and Debugging

### Cache Management Admin

Access the cache management interface at:
- URL: `/admin/cache-management/`
- Access: Superuser only

Features:
- View all cache keys in hierarchical structure
- See cache values (unpickled and displayed as strings)
- Delete individual cache keys
- Clear all cache
- Lazy loading - only loads one level at a time for performance

### Cache Statistics

Currently, the cache management interface shows:
- Total number of cache keys at root level
- Cache backend type
- Individual cache key values

---

## Best Practices

1. **Always invalidate related caches** when updating models
2. **Use appropriate timeouts** based on data volatility
3. **Monitor cache hit rates** (consider adding metrics)
4. **Clear cache after deployments** if schema changes occur
5. **Use cache management admin** for debugging cache issues

---

## Migration Notes

If migrating to a different cache backend (e.g., Redis):

1. Update `CACHES` setting in `server/settings.py`
2. Ensure all cache keys remain compatible
3. Test cache invalidation still works correctly
4. Consider adding cache key prefixes for multi-tenant scenarios
5. Update timeout values if needed for distributed systems

---

## Troubleshooting

### Cache Not Updating

1. Check if cache invalidation is being called in model save/delete methods
2. Verify cache timeout hasn't expired (for time-based expiration)
3. Clear cache manually via admin interface
4. Check for cache key naming mismatches

### Memory Issues

1. Monitor cache size in admin interface
2. Reduce cache timeouts if memory is constrained
3. Consider switching to Redis/Memcached for distributed caching
4. Implement cache size limits if needed

### Performance Issues

1. Check cache hit rates
2. Verify cache timeouts are appropriate
3. Consider increasing cache timeouts for stable data
4. Review cache invalidation frequency

---

## Related Files

- `main/mixin.py` - Cache getter methods
- `main/models/config.py` - Config cache
- `main/models/token.py` - Token cache invalidation
- `main/models/applicant.py` - Applicant cache invalidation
- `main/models/wechat_info.py` - WeChat info cache invalidation
- `main/models/match.py` - Match cache invalidation
- `main/models/task.py` - Task cache invalidation
- `main/admin/system_actions.py` - Cache management admin
- `server/settings.py` - Cache backend configuration

---

*Last updated: 2026-01-27*
